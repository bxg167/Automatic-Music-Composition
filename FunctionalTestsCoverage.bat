py -2 run_coverage.py erase
py -2 run_coverage.py run "./testrunner.py"
del "./htmlcov/" /Q
py -2 run_coverage.py html
pause