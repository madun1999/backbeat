import essentia
import essentia.standard
import essentia.streaming

def get_beat_locations_from_wav_file(file_path):
    """
    Given path to a .wav file, returns a numpy.ndarray of floats corresponding to the seconds of file where beat occurred.
    
    @param file_path: Path to .wav file
    @return: numpy.ndarray of floats corresponding to the seconds of file where beat occurred.
    """
    try:
        #instantiate the audio loader
        loader = essentia.standard.MonoLoader(filename=str(file_path))
        #actually perform the loading
        audio = loader()
    except:
        raise ValueError('Could not load .wav file. Make sure path to file is correct.')
    
    #Generate numpy.ndarray of floats corresponding to seconds of file where beat occurred
    #Not necessary to get overall bpm for file but may be useful if we want to analyze bpm ourselves
    beatTrackerDegara = essentia.standard.BeatTrackerDegara()
    ticks = beatTrackerDegara(audio)
    return ticks

def get_bpm_from_wav_file(file_path, confidence_threshold):
    """
    Given path to a .wav file, returns an estimate of the bpm.

    @param file_path: Path to .wav file
    @param confidence_threshold: Float between 0.0 and 1.0, inclusive, specifying the confidence_threshold necessary to return nonzero estimate for bpm estimation
    @return: estimated bpm. If confidence for the bpm calculation is below the confidence_threshold, returns 0.0
    """

    #Make sure confidence_threshold is valid
    if confidence_threshold < 0.0 or confidence_threshold > 1.0:
        raise ValueError('Confidence threshold must be between 0.0 and 1.0 inclusive')

    try:
        #instantiate the audio loader
        loader = essentia.standard.MonoLoader(filename=str(file_path))
        #actually perform the loading
        audio = loader()
    except:
        raise ValueError('Could not load .wav file. Make sure path to file is correct.')
    
    #Estimate bpm for the whole file. If the confidence is below the threshold, the 
    #estimated bpm will be 0.0.
    loopBpmEstimator = essentia.standard.LoopBpmEstimator(confidenceThreshold=confidence_threshold)
    bpm = loopBpmEstimator(audio)
    return bpm

