# This file contains the backend methods that will process the output of Essentia and provide understandable feedback based on this.
import numpy as np
import analyze_beats
import os

# will return an array of arrays where each index is a chunk of measures and the the first value at that index is the
# BPM of a chunk and the second value is the duration of that chunk im measures. EX:
# [[BPM1, NumMeasure1], [BPM2, NumMeasures2]]
def getMeasures(file_path, beats_per_measure, confidence_threshold):
    beat_arr = analyze_beats.get_beat_locations_from_wav_file(file_path)
    measure_arr = []
    measure_arr.append(0)
    num_measures = 0
    for i in range(0, len(beat_arr)):
        if ((i + 1) % beats_per_measure == 0):
            num_measures += 1
            measure_arr.append(beat_arr[i])
    # NOTE at this point there is a chunk of music after the last location in measure_arr that
    # we also need to analyze but that is not a full measure
    index = 0
    chunk_arr = []
    num_chunks = 0
    while (index < (len(measure_arr) - 1)):
        chunk_length = 1
        chunk_BPM = analyze_beats.get_bpm_from_wav_file(file_path, measure_arr[index], measure_arr[index + chunk_length], confidence_threshold)
        if (index + chunk_length == len(measure_arr) - 1):
            # This goes to the end of our data. Use this regardless of what the BPM returns
            chunk_arr.append([chunk_BPM, chunk_length])
            num_chunks += 1
            break
        while (chunk_BPM == 0 and index + chunk_length < (len(measure_arr) - 1)):
            chunk_length += 1
            chunk_BPM = analyze_beats.get_bpm_from_wav_file(file_path, measure_arr[index], measure_arr[index + chunk_length], confidence_threshold)
        # Either the chunk returns a BPM or it goes until the end of our data
        chunk_arr.append([chunk_BPM, chunk_length])
        num_chunks += 1
        index = index + chunk_length
    return chunk_arr


# Method to determine where the player slowed/sped up and return a string describing this
# Accepts an array of integers each representing the tempo in a given measure and an integer representing the target tempo
# Also accepts an integer representing the allowable margin of error
# temopArr is an array of integers each representing the average tempo of one measure
# targetTempo is the tempo the player was aiming to play at
# marginOfError represents the allowable divergence from the target without a comment
# Returns a string describing the patterns of the musician

def getAnalysis(tempoArr, targetTempo, marginOfError):
    # Create a list of lists. Each sublist will contain a string denoting 'fast' 'slow' or 'steady',
    # an integer that denotes the duration of this action,
    # and an integer that denotes the measure number of the last measure of this behavior
    behaviorList = []
    # Loop through the array of tempos
    # Set up the loop
    steadyDuration = 0
    fastDuration = 0
    slowDuration = 0
    if (tempoArr[0] > (targetTempo + marginOfError)):
        fastDuration = 1
    elif (tempoArr[0] < (targetTempo - marginOfError)):
        slowDuration = 1
    else:
        steadyDuration = 1
    # Start the loop
    for measure in range(1, len(tempoArr)):
        # Fill the list with patches of slowness, fastness, and normalness
        if (steadyDuration > 0):
            # The last measure(s) was steady
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                behaviorList.append(["steady", steadyDuration, measure])
                steadyDuration = 0
                slowDuration = 0
                fastDuration = 1
            elif (tempoArr[measure] < (targetTempo - marginOfError)):
                # This measure is slow
                behaviorList.append(["steady", steadyDuration, measure])
                steadyDuration = 0
                fastDuration = 0
                slowDuration = 1
            else:
                # This measure is steady
                steadyDuration += 1
        elif (fastDuration > 0):
            # The last measure(s) was fast
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                fastDuration += 1
            elif (tempoArr[measure] < (targetTempo - marginOfError)):
                # This measure is slow
                behaviorList.append(["fast", fastDuration, measure])
                steadyDuration = 0
                fastDuration = 0
                slowDuration = 1
            else:
                # This measure is steady
                behaviorList.append(["fast", fastDuration, measure])
                fastDuration = 0
                slowDuration = 0
                steadyDuration = 1
        elif (slowDuration > 0):
            # The last measure(s) was steady
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                behaviorList.append(["slow", slowDuration, measure])
                steadyDuration = 0
                slowDuration = 0
                fastDuration = 1
            elif (tempoArr[measure] < (targetTempo - marginOfError)):
                # This measure is slow
                slowDuration += 1
            else:
                # This measure is steady
                behaviorList.append(["slow", slowDuration, measure])
                slowDuration = 0
                fastDuration = 0
                steadyDuration = 1
    # Add final entry to behaviorList
    if (slowDuration > 1):
        behaviorList.append(["slow", slowDuration, len(tempoArr)])
    elif (fastDuration > 1):
        behaviorList.append(["fast", fastDuration, len(tempoArr)])
    elif (steadyDuration > 1):
        behaviorList.append(["steady", steadyDuration, len(tempoArr)])
    # Concatenate a string that describes the list of lists
    description = ""
    # Create first line (special Case)
    avgTempo = np.average(tempoArr[0:(behaviorList[0][2])])
    if (behaviorList[0][0] == "slow"):
        description = "You started out slow, and were slow for " + str(behaviorList[0][1]) + " measures until measure number " + str(behaviorList[0][2]) + " with an average tempo of " + avgTempo + " BPM.\n"
    elif (behaviorList[0][0] == "fast"):
        description = "You started out fast, and were fast for " + str(behaviorList[0][1]) + " measures until measure number " + str(behaviorList[0][2]) + " with an average tempo of " + avgTempo + " BPM.\n"
    elif (behaviorList[0][0] == "steady"):
        description = "You started our steady, and were steady for " + str(behaviorList[0][1]) + " measures until measure number " + str(behaviorList[0][2]) + " with an average tempo of " + avgTempo + " BPM.\n"
    # Create the description for the second line throgh the second to last line
    for index in  range(1, len(behaviorList) - 1):
        avgTempo = np.average(tempoArr[behaviorList[index - 1][2]:behaviorList[index][2]])
        if (behaviorList[index][0] == "slow"):
            description += "Starting in measure " + str(behaviorList[index - 1][2] + 1) + " you were slow, and were slow for " + str(behaviorList[index][1]) + " measures until measure number " + str(behaviorList[index][2]) + " with an average tempo of " + avgTempo + " BPM.\n"
        elif (behaviorList[index][0] == "fast"):
            description += "Starting in measure " + str(behaviorList[index - 1][2] + 1) + " you were fast, and were fast for " + str(behaviorList[index][1]) + " measures until measure number " + str(behaviorList[index][2]) + " with an average tempo of " + avgTempo + " BPM.\n"
        elif (behaviorList[index][0] == "steady"):
            description += "Starting in measure " + str(behaviorList[index - 1][2] + 1) + " you were steady, and were steady for " + str(behaviorList[index][1]) + " measures until measure number " + str(behaviorList[index][2]) + " with an average tempo of " + avgTempo + " BPM.\n"
    # Create the description of the final line
    avgTempo = np.average(tempoArr[behaviorList[index - 1][2]:behaviorList[index][2]])
    if (behaviorList[len(behaviorList) - 1][0] == "slow"):
        description += "Starting in measure " + str(behaviorList[len(behaviorList) - 2][2] + 1) + " you were slow, and were slow for " + str(behaviorList[len(behaviorList) - 1][1]) + " measures until the end of the piece with an average tempo of " + avgTempo + " BPM.\n"
    elif (behaviorList[len(behaviorList) - 1][0] == "fast"):
        description += "Starting in measure " + str(behaviorList[len(behaviorList) - 2][2] + 1) + " you were fast, and were fast for " + str(behaviorList[len(behaviorList) - 1][1]) + " measures until the end of the piece with an average tempo of " + avgTempo + " BPM.\n"
    elif (behaviorList[len(behaviorList) - 1][0] == "steady"):
        description += "Starting in measure " + str(behaviorList[len(behaviorList) - 2][2] + 1) + " you were steady, and were steady for " + str(behaviorList[len(behaviorList) - 1][1]) + " measures until the end of the piece with an average tempo of " + avgTempo + " BPM.\n"
    # Return this string
    return description


class Ranges(object):
    cups = 0  # class variable. This belongs to the class

    # __init__ is (basically) a constructor.
    def __init__(self, speed, start, end):
        self.speed = speed  # These are instance variables. these belong to the object
        self.start = start
        self.end = end

        # Instance method

    def get_range (self):
        return self.start, self.end


    @classmethod  # use decorator @staticmethod to create static methods
    def get_speed(self):
        return self.speed

def speedRange(tempoArr, targetTempo, marginOfError, sigSpeedRange):
    # Create a list of lists. Each sublist will contain a string denoting 'fast' 'slow' or 'steady',
    # an integer that denotes the duration of this action,
    # and an integer that denotes the measure number of the last measure of this behavior
    rangeList = []
    # Loop through the array of tempos
    # Set up the loop
    steadyDuration = 0
    fastDuration = 0
    slowDuration = 0
    fastStart = 0
    slowStart = 0
    numOfFast = 0
    numOfSlow = 0
    counter = 0
    if (tempoArr[0] > (targetTempo + marginOfError)):
        fastDuration = 1
    elif (tempoArr[0] < (targetTempo - marginOfError)):
        slowDuration = 1
    else:
        steadyDuration = 1
    # Start the loop
    for measure in range(1, len(tempoArr)):
        # Fill the list with patches of slowness, fastness, and normalness
        if (steadyDuration > 0):
            # The last measure(s) was steady
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                steadyDuration = 0
                slowDuration = 0
                fastDuration = 1
                fastStart = measure
                numOfFast += 1

            elif (tempoArr[measure] < (targetTempo - marginOfError)):
                # This measure is slow
                steadyDuration = 0
                fastDuration = 0
                slowDuration = 1
                slowStart = measure
                numOfSlow += 1
            else:
                # This measure is steady
                steadyDuration += 1
                fastStart = 0
                slowStart = 0
                numOfSlow = 0
                numOfFast = 0
        elif (fastDuration > 0):
            # The last measure(s) was fast
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                fastDuration += 1
                numOfFast += 1
            elif (tempoArr[measure] < (targetTempo - marginOfError)):
                # This measure is slow
                steadyDuration = 0
                fastDuration = 0
                slowDuration = 1
                if sigSpeedRange <= numOfFast:
                    rangeList[counter] = Ranges("Fast",fastStart, measure - 1)
                    counter += 1
                numOfFast = 0
                fastStart = 0
                slowStart = measure
            else:
                # This measure is steady
                if sigSpeedRange <= numOfFast:
                    rangeList[counter] = Ranges("Fast",fastStart, measure - 1)
                    counter +=1
                numOfFast = 0
                fastStart = 0
                fastDuration = 0
                slowDuration = 0
                steadyDuration = 1
        elif (slowDuration > 0):
            # The last measure(s) was slow
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                steadyDuration = 0
                slowDuration = 0
                fastDuration = 1
                if sigSpeedRange <= numOfFast:
                    rangeList[counter] = Ranges("Fast",fastStart, measure - 1)
                    counter +=1

            elif (tempoArr[measure] < (targetTempo - marginOfError)):
                # This measure is slow
                slowDuration += 1
                numOfSlow += 1

            else:
                # This measure is steady
                slowDuration = 0
                fastDuration = 0
                steadyDuration = 1
                fastStart = 0
                slowStart = 0
                numOfSlow = 0
                numOfFast = 0
    return rangeList

# method to return an array of integers which each represent the tempo in a single measure of the piece.
# audioFile is the mp3/wav file to be analyzed
# beatsPerMeasure is the number of beats in a measure
# tempoEstimate is the tempo the player is aiming to play at.
# Returns an array of integers that represents the tempo of each measure.
#import bpmHistogram
def getTempos(audioFile, beatsPerMeasure, tempoEstimate):
    # TODO define this method as pseudocode
    pass
