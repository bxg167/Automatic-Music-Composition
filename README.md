# Automatic-Music-Composition

This project was implemented as a Software Engineering course assignment.

##Product Overview
The Automatic Music Composition System is a three-part program that creates musical compositions,
using a recurrent neural network (RNN) and a large library of MIDI files. When given a library of MIDI files,
the program extracts single voice/instrument tracks from the MIDI file and stores it for later use.
Once all of the voices are separated from the MIDI files, the RNN will be taught how to create compositions by
training on these separated files. Once the RNN has a good understanding of music, the user will be able to make
the RNN compose a unique piece of music.

##Component Descriptions
The three components of the program are as follows:
####File Converter
- The first component converts midi tracks into Readable Conversion File Format, a format that is neural network-readable.
The converted files are stored as .rcff.
####Neural Network Trainer
- The second component trains a neural network using RCFF files. This portion of the program can be very computation
and time intensive. The component also generates new RCFF files from a trained network.
####Music Composer
- The final component takes a snapshot of a trained neural network and runs it to generate a new piece of music,
which is converted back to midi so that the user may listen to it.

_Executables to run the components can be found in \bin\dist_

##Code Requirements
This project was implemented in Python, but to make things complicated, we had to use both 2.7 and 3.5.

#### MIDI Conversion Environment
- Python 2.7
- Python-Midi library
#### Neural Network Environment
- Python 3.5
- Tensorflow library