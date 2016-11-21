::Test case 3.2.7 has not been implemented, since it sort of requires the actual program to be built.

@ECHO OFF

"C:\python27\python.exe" run_coverage.py erase

cls
echo Case 3.2.1a and Case 3.2.6a
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file"
pause
del ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file\default.snapshot"

cls
echo Case 3.2.1b
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\-1 files"
pause

cls
echo Case 3.2.1c
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\0 files"
pause

cls
echo Case 3.2.2
echo Make sure that there is no snapshot.snapshot in the window the opened.
explorer ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files"
pause

"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file" -S ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\snapshot.snapshot"
pause
del ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\snapshot.snapshot"

cls
echo Case 3.2.3
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file" -S ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\duplicate_snapshot.snapshot"
pause

cls
echo Case 3.2.4
echo Check what the size of the existing duplicate_snapshot.snapshot is.
explorer ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files"
pause
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file" -U ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\duplicate_snapshot.snapshot"

echo Check what the size of the existing duplicate_snapshot.snapshot is again (It should be bigger than before)
pause

cls
echo Case 3.2.4b
echo Not included in the submitted test document. Test for an error being raised when an incorrect path is passed with -update
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file" -U ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\no_snapshot.snapshot"
pause

cls
echo Case 3.2.5
echo Make sure that there is no default.snapshot in the window the opened.
explorer ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file"
pause

"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file"
pause
del ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file\default.snapshot"

cls
echo Case 3.2.6b
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -R ".\Tests\Functional_Tests\Functional_Test_Files\Teacher RCFF files\1 file" -S ".\Fake\Folder\that\doesnt\exist\snapshot.snapshot
pause

cls
echo Case 3.2.8
"C:\python27\python.exe" run_coverage.py run -a .\GUI\TeacherCommandLine.py -h
pause
cls

@Echo on
del "./htmlcov/" /Q
"C:\python27\python.exe" run_coverage.py html
pause