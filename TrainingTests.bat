py -3 run_coverage.py erase
py -3 run_coverage.py run -a "./Training/Unit Tests/test_tflstm.py"
py -3 run_coverage.py run -a "./Training/Functional Tests/tests_File_Playback.py"
py -3 run_coverage.py run -a "./Training/Functional Tests/tests_Training.py"
del "./htmlcov/" /Q
py -3 run_coverage.py html
pause