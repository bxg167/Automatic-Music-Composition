cd ..
py -2 setup.py install

cd bin
C:\python27\scripts\pyinstaller --windowed --clean --onefile --p "..\GUI" --p "..\File_Conversion" ..\GUI\ConverterGui.py
.\dist\ConverterGui.exe
pause