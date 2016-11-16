from pythonforandroid.recipe import CompiledComponentsPythonRecipe
from os.path import join

class NetifacesRecipe(CompiledComponentsPythonRecipe):
    name = 'netifaces'
    version = '0.10.4'
    url = 'https://pypi.python.org/packages/source/n/netifaces/netifaces-{version}.tar.gz'
    site_packages_name = 'netifaces'
    depends = [('python2', 'python3crystax'), 'setuptools']
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch):
        env = super(NetifacesRecipe, self).get_recipe_env(arch)
        env['CFLAGS'] += ' -I' + join(self.ctx.get_python_install_dir(), 'include/python2.7')
        env['LDSHARED'] = env['CC'] + ' -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions'
        env['LDFLAGS'] += ' -lpython2.7'
        return env



recipe = NetifacesRecipe()
