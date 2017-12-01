import essentia
import essentia.standard
import essentia.streaming
import wave
import contextlib
from collections import OrderedDict

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

def get_bpm_from_wav_file(file_path, confidence_threshold, start_time=None, end_time=None):
    """
    Given path to a .wav file, returns an estimate of the bpm.

    @param file_path: Path to .wav file
    @param confidence_threshold: Float between 0.0 and 1.0, inclusive, specifying the confidence_threshold necessary to return nonzero estimate for bpm estimation
    @param start_time: starting time in seconds of segment to analyze bpm
    @param end_time: ending time in seconds of segment to analyze bpm
    @return: estimated bpm. If confidence for the bpm calculation is below the confidence_threshold, returns 0.0
    """

    #Make sure confidence_threshold is valid
    if confidence_threshold < 0.0 or confidence_threshold > 1.0:
        raise ValueError('Confidence threshold must be between 0.0 and 1.0 inclusive')

    try:
        #instantiate the audio loader
        loader = essentia.standard.EasyLoader(filename=str(file_path), startTime=start_time, endTime=end_time)
        #actually perform the loading
        audio = loader()
    except:
        raise ValueError('Could not load .wav file. Make sure path to file is correct.' + '\nFile path: ' + str(file_path))

    #Estimate bpm for the whole file. If the confidence is below the threshold, the
    #estimated bpm will be 0.0.
    loopBpmEstimator = essentia.standard.LoopBpmEstimator(confidenceThreshold=confidence_threshold)
    bpm = loopBpmEstimator(audio)
    return bpm


def get_length_of_wav_file_seconds(file_path):
    #this method was derived from https://stackoverflow.com/questions/7833807/get-wav-file-length-or-duration
    fname = file_path
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration


def get_bpm_for_constant_fractions_of_wav_file(file_path, confidence_threshold, num_divisions):
    #Make sure confidence_threshold is valid
    if confidence_threshold < 0.0 or confidence_threshold > 1.0:
        raise ValueError('Confidence threshold must be between 0.0 and 1.0 inclusive')

    if num_divisions <= 0:
        raise ValueError('num_divisions must be greater than 0')

    length_sec = get_length_of_wav_file_seconds(file_path)

    bpm_chunks_dict = OrderedDict()

    for i in range(0, num_divisions):
        start_audio = length_sec * (i / float(num_divisions))
        end_audio = length_sec * ((i + 1) / float(num_divisions))
        time_range_tuple = (start_audio, end_audio)

        #In the output dictionary, values are bpms and keys are their associated time ranges
        current_bpm = get_bpm_from_wav_file(file_path, confidence_threshold, start_audio, end_audio)
        bpm_chunks_dict[time_range_tuple] = current_bpm

    return bpm_chunks_dict

def get_audio_from_wav_path(file_path):
    """
    Given path to a .wav file, returns the loaded audio array

    @param file_path: Path to .wav file
    @return: audio object
    """
    try:
        #instantiate the audio loader
        loader = essentia.standard.EasyLoader(filename=str(file_path))
        #actually perform the loading
        audio = loader()
        return audio
    except:
        raise ValueError('Could not load .wav file. Make sure path to file is correct.' + '\nFile path: ' + str(file_path))


def get_bpm_from_audio_array(audio, confidence_threshold, start_time, end_time, total_audio_length_sec):
    """
    Given a pre-loaded audio object, find bpm based on given parameters.

    @param audio: audio object that was already loaded from a wav file
    @param confidence_threshold: Float between 0.0 and 1.0, inclusive, specifying the confidence_threshold necessary to return nonzero estimate for bpm estimation
    @param start_time: starting time in seconds of segment to analyze bpm
    @param end_time: ending time in seconds of segment to analyze bpm
    @param total_audio_length_sec: length of audio file in seconds
    @return: estimated bpm. If confidence for the bpm calculation is below the confidence_threshold, returns 0.0
    """

    #Make sure confidence_threshold is valid
    if confidence_threshold < 0.0 or confidence_threshold > 1.0:
        raise ValueError('Confidence threshold must be between 0.0 and 1.0 inclusive')

    total_frames = len(audio)
    start_frame = int(round((start_time / float(total_audio_length_sec)) * total_frames))
    end_frame = int(round((end_time / float(total_audio_length_sec)) * total_frames))

    #If the confidence is below the threshold, the estimated bpm will be 0.0.
    loopBpmEstimator = essentia.standard.LoopBpmEstimator(confidenceThreshold=confidence_threshold)
    bpm = loopBpmEstimator(audio[start_frame : end_frame])
    return bpm

