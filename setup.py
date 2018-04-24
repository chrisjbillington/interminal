from distutils.core import setup
import sys

VERSION = '0.3.6'

setup(name='interminal',
      version=VERSION,
      description='Utility for launching commands in a GUI terminal',
      author='Chris Billington',
      author_email='chrisjbillington@gmail.com',
      url='https://github.com/chrisjbillington/interminal',
      license="BSD",
      scripts=['bin/interminal', 'bin/inshell'],
      install_requires=['pexpect'],)
