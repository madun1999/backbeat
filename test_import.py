from analyze_beats import*
from backend import*

fname = 'sample_wav_files/air_force_song.wav'
print(get_length_of_wav_file_seconds(fname))

print(get_bpm_from_wav_file(fname, 0.0, 10, 45))
#print(getMeasures('sample_wav_files/air_force_song.wav', 4, 0.25))





