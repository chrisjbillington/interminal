from distutils.core import setup
import sys

if sys.version_info < (3, 0):
    raise Exception('Python >= 3 required')

VERSION = '0.2.5'


setup(name='interminal',
      version=VERSION,
      description='Utility for launching commands in a GUI terminal',
      author='Chris Billington',
      author_email='chrisjbillington@gmail.com',
      url='https://github.com/chrisjbillington/interminal',
      license="BSD",
      scripts=['bin/interminal', 'bin/inshell'])
