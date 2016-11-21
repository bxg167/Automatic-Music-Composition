:: The coverage is consumed with the combine process, so make a copy of the file BEFORE YOU COMBINE

copy ComposerGUI.coverage "ComposerGUI - copy.coverage"

copy ConverterGUI.coverage "ConverterGUI - copy.coverage"

copy TeacherCMD.coverage "TeacherCMD - copy.coverage"

copy FunctionalTest.coverage "FunctionalTest - copy.coverage"

pause

"C:\python27\python.exe" run_coverage.py erase
"C:\python27\python.exe" run_coverage.py combine "ComposerGUI - copy.coverage" "ConverterGUI - copy.coverage" "TeacherCMD - copy.coverage" "FunctionalTest - copy.coverage"

del "./htmlcov/" /Q
"C:\python27\python.exe" run_coverage.py html
pause