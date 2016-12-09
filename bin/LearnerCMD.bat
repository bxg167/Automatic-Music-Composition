cd ..
py -3 setup.py install

cd bin
"C:\Program Files\Python35\Scripts\pyinstaller" --clean --onefile --p "..\GUI" --p "..\Training" --p "..\File_Conversion" ..\GUI\TeacherCommandLine.py
.\dist\TeacherCommandLine.exe --teach "C:\Users\Bryce\Desktop\130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]\1\RCFF_Files"
pause