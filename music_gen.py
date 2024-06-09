# you need to manually install the PySynth library from GitHub (pip is outdated)
# https://stackoverflow.com/questions/75492840/attributeerror-module-pysynth-has-no-attribute-make-wav
import PySynth.pysynth as pysynth

def parse_notes(file_path):
    """
    Parses a text file to extract musical notes and their lengths.
    Expects each line in the file to be in the format 'note length', e.g., 'c#4 4'.
    """
    notes = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                note, length = parts
                notes.append((note, int(length)))
    return notes

def generate_music(notes, output_file):
    pysynth.make_wav(notes, fn=output_file)
    print(f"Generated music saved to {output_file}")

default_file_path = 'music.txt'

if __name__ == "__main__":
    notes = parse_notes(default_file_path)
    generate_music(notes, "output.wav")

