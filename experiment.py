import essentia
import essentia.standard
import essentia.streaming

#instantiate the audio loader; this file is in the current directory
loader = essentia.standard.MonoLoader(filename='air_force_song.wav')

#actually perform the loading
audio = loader()

print('\nThe audio signal:\n' + str(audio))
print('\nThe length of audio signal is: ' + str(len(audio)))

#Generate numpy.ndarray of floats corresponding to seconds of file where beat occurred
#Not necessary to get overall bpm for file but may be useful if we want to analyze bpm ourselves
#beatTrackerDegara = essentia.standard.BeatTrackerDegara()
#ticks = beatTrackerDegara(audio)
#print('\nEstimated location of beats:\n' + str(ticks))

loopBpmEstimator1 = essentia.standard.LoopBpmEstimator(confidenceThreshold=0.2)
bpm = loopBpmEstimator1(audio[:len(audio)/5])
print('\nTHE ESTIMATED BPM for first part: ' + str(bpm))

loopBpmEstimator2 = essentia.standard.LoopBpmEstimator(confidenceThreshold=0.2)
bpm = loopBpmEstimator2(audio[len(audio)*.7:len(audio)*.99])
print('THE ESTIMATED BPM for second part is: ' + str(bpm))







