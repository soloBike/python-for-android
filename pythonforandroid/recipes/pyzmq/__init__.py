# coding=utf-8

from pythonforandroid.recipe import CythonRecipe, Recipe
from os.path import join
from pythonforandroid.util import current_directory
import sh
from pythonforandroid.logger import shprint
import glob


class PyZMQRecipe(CythonRecipe):
    name = 'pyzmq'
    version = 'master'
    url = 'https://github.com/zeromq/pyzmq/archive/{version}.zip'
    site_packages_name = 'zmq'
    depends = [('python2', 'python3crystax'), 'libzmq']
    cython_args = ['-Izmq/utils',
                   '-Izmq/backend/cython',
                   '-Izmq/devices']
    patches = ["fix-import.patch"]

    def build_cython_components(self, arch):
        libzmq_recipe = Recipe.get_recipe('libzmq', self.ctx)
        libzmq_prefix = join(libzmq_recipe.get_build_dir(arch.arch), "install")
        self.setup_extra_args = ["--zmq={}".format(libzmq_prefix)]
        self.build_cmd = "configure"

        env = self.get_recipe_env(arch)
        setup_cfg = join(self.get_build_dir(arch.arch), "setup.cfg")
        with open(setup_cfg, "wb") as fd:
            fd.write("""
[global]
zmq_prefix = {}
skip_check_zmq = True
""".format(libzmq_prefix))

        return super(PyZMQRecipe, self).build_cython_components(arch)

        with current_directory(self.get_build_dir(arch.arch)):
            hostpython = sh.Command(self.hostpython_location)
            shprint(hostpython, 'setup.py', 'configure', '-v', _env=env)
            shprint(hostpython, 'setup.py', 'build_ext', '-v', _env=env)
            build_dir = glob.glob('build/lib.*')[0]
            shprint(sh.find, build_dir, '-name', '"*.o"', '-exec',
                    env['STRIP'], '{}', ';', _env=env)

recipe = PyZMQRecipe()
