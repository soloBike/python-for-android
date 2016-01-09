from os.path import (join)
from os import environ, uname
import sys
from distutils.spawn import find_executable

from pythonforandroid.logger import warning
from pythonforandroid.recipe import Recipe


class Arch(object):

    toolchain_prefix = None
    '''The prefix for the toolchain dir in the NDK.'''

    command_prefix = None
    '''The prefix for NDK commands such as gcc.'''

    def __init__(self, ctx):
        super(Arch, self).__init__()
        self.ctx = ctx

    def __str__(self):
        return self.arch

    @property
    def include_dirs(self):
        return [
            "{}/{}".format(
                self.ctx.include_dir,
                d.format(arch=self))
            for d in self.ctx.include_dirs]

    def get_env(self):
        env = {}

        env["CFLAGS"] = " ".join([
            "-DANDROID", "-mandroid", "-fomit-frame-pointer",
            "--sysroot", self.ctx.ndk_platform])

        env["CXXFLAGS"] = env["CFLAGS"]

        env["LDFLAGS"] = " ".join(['-lm'])

        py_platform = sys.platform
        if py_platform in ['linux2', 'linux3']:
            py_platform = 'linux'

        toolchain_prefix = self.ctx.toolchain_prefix
        toolchain_version = self.ctx.toolchain_version
        command_prefix = self.command_prefix

        env['TOOLCHAIN_PREFIX'] = toolchain_prefix
        env['TOOLCHAIN_VERSION'] = toolchain_version

        print('path is', environ['PATH'])
        cc = find_executable('{command_prefix}-gcc'.format(
            command_prefix=command_prefix), path=environ['PATH'])
        if cc is None:
            warning('Couldn\'t find executable for CC. This indicates a '
                    'problem locating the {} executable in the Android '
                    'NDK, not that you don\'t have a normal compiler '
                    'installed. Exiting.')
            exit(1)

        env['CC'] = '{command_prefix}-gcc {cflags}'.format(
            command_prefix=command_prefix,
            cflags=env['CFLAGS'])
        env['CXX'] = '{command_prefix}-g++ {cxxflags}'.format(
            command_prefix=command_prefix,
            cxxflags=env['CXXFLAGS'])

        env['AR'] = '{}-ar'.format(command_prefix)
        env['RANLIB'] = '{}-ranlib'.format(command_prefix)
        env['LD'] = '{}-ld'.format(command_prefix)
        # env['LDSHARED'] = join(self.ctx.root_dir, 'tools', 'liblink')
        # env['LDSHARED'] = env['LD']
        env['STRIP'] = '{}-strip --strip-unneeded'.format(command_prefix)
        env['MAKE'] = 'make -j5'
        env['READELF'] = '{}-readelf'.format(command_prefix)

        hostpython_recipe = Recipe.get_recipe('hostpython2', self.ctx)

        # AND: This hardcodes python version 2.7, needs fixing
        env['BUILDLIB_PATH'] = join(
            hostpython_recipe.get_build_dir(self.arch),
            'build', 'lib.linux-{}-2.7'.format(uname()[-1]))

        env['PATH'] = environ['PATH']

        env['ARCH'] = self.arch

        if self.ctx.ndk_is_crystax:  # AND: should use the right python version from the python recipe
            env['CRYSTAX_PYTHON_VERSION'] = '3.5'

        return env


class ArchARM(Arch):
    arch = "armeabi"
    toolchain_prefix = 'arm-linux-androideabi'
    command_prefix = 'arm-linux-androideabi'
    platform_dir = 'arch-arm'


class ArchARMv7_a(ArchARM):
    arch = 'armeabi-v7a'

    def get_env(self):
        env = super(ArchARMv7_a, self).get_env()
        env['CFLAGS'] = (env['CFLAGS'] +
                         (' -march=armv7-a -mfloat-abi=softfp '
                          '-mfpu=vfp -mthumb'))
        env['CXXFLAGS'] = env['CFLAGS']
        return env


class Archx86(Arch):
    arch = 'x86'
    toolchain_prefix = 'x86'
    command_prefix = 'i686-linux-android'
    platform_dir = 'arch-x86'

    def get_env(self):
        env = super(Archx86, self).get_env()
        env['CFLAGS'] = (env['CFLAGS'] +
                         ' -march=i686 -mtune=intel -mssse3 -mfpmath=sse -m32')
        env['CXXFLAGS'] = env['CFLAGS']
        return env


class Archx86_64(Arch):
    arch = 'x86_64'
    toolchain_prefix = 'x86'
    command_prefix = 'x86_64-linux-android'
    platform_dir = 'arch-x86'

    def get_env(self):
        env = super(Archx86_64, self).get_env()
        env['CFLAGS'] = (env['CFLAGS'] +
                         ' -march=x86-64 -msse4.2 -mpopcnt -m64 -mtune=intel')
        env['CXXFLAGS'] = env['CFLAGS']
        return env
