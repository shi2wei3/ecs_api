import os
from distutils.core import Command
from setuptools import setup, find_packages

name = 'ecs_api'
version = '0.1'


class RPMCommand(Command):
    description = "Build src and binary rpms."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """
        Run sdist, then 'rpmbuild' the tar.gz
        """
        os.system("cp %s.spec /tmp" % name)
        try:
            os.system("rm -rf %s-%s" % (name, version))
            self.run_command('sdist')
            os.system('rpmbuild -ta --clean dist/%s-%s.tar.gz' %
                      (name, version))
        finally:
            os.system("mv /tmp/%s.spec ." % name)


setup(name=name,
      version=version,
      description='ECS API',
      long_description='ECS API',
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Wei Shi',
      author_email='wshi@redhat.com',
      license="GPLv2",
      url='https://github.com/shi2wei3/ecs_api',
      keywords='ecs api',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      requires=['requests', ],
      cmdclass={
        "rpm": RPMCommand
      },
      entry_points="""\
      [console_scripts]
      ecs = ecs_api.ecs:main
      """
      )
