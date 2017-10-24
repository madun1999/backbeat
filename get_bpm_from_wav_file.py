import essentia
import essentia.standard
import essentia.streaming

#instantiate the audio loader; this file is in the current directory
loader = essentia.standard.MonoLoader(filename='air_force_song.wav')

#actually perform the loading
audio = loader()

print('\nThe audio signal:\n' + str(audio))

#Generate numpy.ndarray of floats corresponding to seconds of file where beat occurred
#Not necessary to get overall bpm for file but may be useful if we want to analyze bpm ourselves
beatTrackerDegara = essentia.standard.BeatTrackerDegara()
ticks = beatTrackerDegara(audio)
print('\nEstimated location of beats:\n' + str(ticks))

#Estimate bpm for the whole file. If the confidence is below the threshold, the 
#estimated bpm will be 0.0. The default threshold is 0.95 but the audio file I am using
#slows down slightly at the end, so I reduced the confidence level to get a impressively
#accurate bpm of 115.0
loopBpmEstimator = essentia.standard.LoopBpmEstimator(confidenceThreshold=0.85)
bpm = loopBpmEstimator(audio)
print('\nTHE ESTIMATED BPM IS: ' + str(bpm))
