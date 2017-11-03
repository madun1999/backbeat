from analyze_beats import*
from backend import*

fname = 'sample_wav_files/air_force_song.wav'
#print(getMeasures('sample_wav_files/africa-toto.wav', 4, 0.95))
print(getMeasures('sample_wav_files/air_force_song.wav', 4, 0.95))
#print(get_bpm_for_constant_fractions_of_wav_file(fname, 0.0, 6))

