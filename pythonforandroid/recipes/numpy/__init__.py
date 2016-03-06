
from pythonforandroid.toolchain import CompiledComponentsPythonRecipe, warning
from pythonforandroid.util import current_directory
from glob import glob

class NumpyRecipe(CompiledComponentsPythonRecipe):

    version = '1.9.2'
    url = 'http://pypi.python.org/packages/source/n/numpy/numpy-{version}.tar.gz'
    site_packages_name= 'numpy'

    depends = ['python2']

    patches = ['patches/fix-numpy.patch',
               'patches/prevent_libs_check.patch',
               'patches/ar.patch',
               'patches/lib.patch']

    def prebuild_arch(self, arch):
        super(NumpyRecipe, self).prebuild_arch(arch)

        # AND: Fix this warning!
        warning('Numpy is built assuming the archiver name is '
                'arm-linux-androideabi-ar, which may not always be true!')

    def install_python_package(self, arch):
        super(NumpyRecipe, self).install_python_package(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            self.install_libs(arch, glob("build/temp.*/libnpymath.a")[0])
            self.install_libs(arch, glob("build/temp.*/libnpysort.a")[0])

recipe = NumpyRecipe()
