from distutils.core import setup
import sys
import pip

if sys.version_info[:2][0] == 2:
      print('2')
      packages_to_install = ["pyinstaller",
                             "coverage",
                             "python-midi",
                             "pypiwin32"]
      for package in packages_to_install:
            pip.main(["install", package])

      setup(name='AMC',
            version='1.0',
            packages=['File_Conversion', 'GUI'],
            )
elif sys.version_info[:2][0] == 3:
      print('3')
      packages_to_install = []
      for package in packages_to_install:
            pip.main(["install", package])
      setup(name='AMC',
            version='1.0',
            packages=['File_Conversion', 'Training'],
            )
else:
      print('None')
