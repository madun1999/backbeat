import analyze_beats
import backend
from timeit import Timer

fname = 'sample_wav_files/air_force_song.wav'
#fname = 'sample_wav_files/africa-toto.wav'

print('getMeasures loading audio every time: ')
t = Timer("""backend.getMeasures('sample_wav_files/air_force_song.wav', 4, 0.95)""", setup="""import backend""")
print t.timeit(1)

print(backend.getMeasures('sample_wav_files/air_force_song.wav', 4, 0.95))
#print(get_bpm_for_constant_fractions_of_wav_file(fname, 0.0, 4))

#audio = get_audio_from_wav_path(fname)
#length = get_length_of_wav_file_seconds(fname)

#for i in range(0, 4):
#    start = i*10
#    end = i*10 + 10
#    print(get_bpm_from_audio_array(audio, 0.0, start, end, length))
