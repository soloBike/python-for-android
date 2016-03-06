from pythonforandroid.toolchain import Recipe, shprint, shutil, current_directory
from pythonforandroid.util import ensure_dir
from os.path import exists, join
import sh


class LibZMQRecipe(Recipe):
    version = '4.1.4'
    url = 'http://download.zeromq.org/zeromq-{version}.tar.gz'
    depends = ['python2']

    def should_build(self, arch):
        return True
        return self.has_libs(arch, 'libzmq.so', 'libgnustl_shared.so')

    def build_arch(self, arch):
        super(LibZMQRecipe, self).build_arch(arch)
        env = self.get_recipe_env(arch)
        #
        # libsodium_recipe = Recipe.get_recipe('libsodium', self.ctx)
        # libsodium_dir = libsodium_recipe.get_build_dir(arch.arch)
        # env['sodium_CFLAGS'] = '-I{}'.format(join(
        #     libsodium_dir, 'src'))
        # env['sodium_LDLAGS'] = '-L{}'.format(join(
        #     libsodium_dir, 'src', 'libsodium', '.libs'))

        curdir = self.get_build_dir(arch.arch)
        prefix = join(curdir, "install")
        with current_directory(curdir):
            bash = sh.Command('sh')
            shprint(
                bash, './configure',
                '--host=arm-linux-androideabi',
                '--without-documentation',
                '--prefix={}'.format(prefix),
                '--with-libsodium=no',
                _env=env)
            shprint(sh.make, _env=env)
            shprint(sh.make, 'install', _env=env)

            gnustl_shared = '{}/sources/cxx-stl/gnu-libstdc++/4.8/libs/{}/libgnustl_shared.so'.format(
                self.ctx.ndk_dir, arch)
            self.install_libs(arch, 'install/lib/libzmq.so', gnustl_shared)

    def get_recipe_env(self, arch):
        # XXX should stl be configuration for the toolchain itself?
        env = super(LibZMQRecipe, self).get_recipe_env(arch)
        env['CFLAGS'] += ' -Os'
        env['CXXFLAGS'] += ' -Os -fPIC -fvisibility=default'
        env['CXXFLAGS'] += ' -I{}/sources/cxx-stl/gnu-libstdc++/4.8/include'.format(self.ctx.ndk_dir)
        env['CXXFLAGS'] += ' -I{}/sources/cxx-stl/gnu-libstdc++/4.8/libs/{}/include'.format(
            self.ctx.ndk_dir, arch)
        env['CXXFLAGS'] += ' -L{}/sources/cxx-stl/gnu-libstdc++/4.8/libs/{}'.format(
            self.ctx.ndk_dir, arch)
        env['CXXFLAGS'] += ' -lgnustl_shared'
        env['LDFLAGS'] += ' -L{}/sources/cxx-stl/gnu-libstdc++/4.8/libs/{}'.format(
            self.ctx.ndk_dir, arch)
        return env


recipe = LibZMQRecipe()
