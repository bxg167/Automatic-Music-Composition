py -2 setup.py install
py -2 run_coverage.py erase
py -2 run_coverage.py run ./Tests/testrunner.py -m --source="C:/Users/Bryce/PycharmProjects/Automatic-Music-Composition/Automatic-Music-Composition/File_Conversion/ConvertRcffToMidi.py"
del "./htmlcov/" /Q
py -2 run_coverage.py html
pause