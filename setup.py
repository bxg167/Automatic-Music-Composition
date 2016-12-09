from distutils.core import setup
import sys

if sys.version_info[:2][0] == 2:
      print('2')
      setup(name='AMC',
            version='1.0',
            packages=['File_Conversion', 'GUI'],
            )
elif sys.version_info[:2][0] == 3:
      print('3')
      setup(name='AMC',
            version='1.0',
            packages=['File_Conversion', 'Training'],
            )
else:
      print('None')
