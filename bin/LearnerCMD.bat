cd ..
py -3 setup.py install

cd bin
"C:\Program Files\Python35\Scripts\pyinstaller" --hidden-import tensorflow --clean --onefile --p "..\GUI" --p "..\Training" --p "..\File_Conversion" --p "C:\Program Files\Python35\Lib"  ..\GUI\TeacherCommandLine.py


::.\dist\TeacherCommandLine.exe --teach "C:\Users\Bryce\Desktop\130000_Pop_Rock_Classical_Videogame_EDM_MIDI_Archive[6_19_15]\1\RCFF_Files"

pause