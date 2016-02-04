import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


requires = [
    'Flask',
    'gdata==2.0.17',
    'lxml',
    'oursql',
    'pymongo'
    ]

setup(name='rnr',
      version='0.1',
      description='Web framework',
      author='Sonali',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      dependency_links = [
        "http://peak.telecommunity.com/snapshots/"
      ],
      )
