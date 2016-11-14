"C:\python27\python.exe" run_coverage.py erase
"C:\python27\python.exe" run_coverage.py run -a .\GUI\convertergui.py
"C:\python27\python.exe" run_coverage.py run -a .\Tests\testrunner.py
"C:\python27\python.exe" run_coverage.py html
pause