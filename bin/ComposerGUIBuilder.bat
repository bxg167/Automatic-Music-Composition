cd ..
py -2 setup.py install

cd bin
C:\python27\scripts\pyinstaller --clean --onefile --p "..\GUI" --p "..\File_Conversion" ..\GUI\ComposerGui.py
.\dist\ComposerGui.exe
pause