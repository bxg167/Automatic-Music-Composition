"C:\python27\python.exe" run_coverage.py erase
"C:\python27\python.exe" run_coverage.py run -a .\GUI\composergui.py

del "./htmlcov/" /Q
"C:\python27\python.exe" run_coverage.py html
pause