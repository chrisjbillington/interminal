from distutils.core import setup

VERSION = '0.2.0'

setup(name='interminal',
      version=VERSION,
      description='Utility for launching commands in a GUI terminal',
      author='Chris Billington',
      author_email='chrisjbillington@gmail.com',
      url='https://github.com/chrisjbillington/interminal',
      license="BSD",
      scripts=['bin/interminal', 'bin/inshell'])
