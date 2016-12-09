py -2 run_coverage.py erase
py -2 run_coverage.py run --source="C:\python27\lib" "./testrunner.py"
py -2 run_coverage.py report
del "./htmlcov/" /Q
py -2 run_coverage.py html
pause