# This file contains the backend methods that will process the output of Essentia and provide understandable feedback based on this.

# Method to determine where the player slowed/sped up and return a string describing this.
# Accepts an array of integers each representing the tempo in a given measure and an integer representing the target tempo.
# Also accepts an integer representing the allowable margin of error. 
# temopArr is an array of integers each representing the average tempo of one measure.
# targetTempo is the tempo the player was aiming to play at.
# marginOfError represents the allowable divergence from the target without a comment.
# Returns a string describing the patterns of the musician
def getAnalysis(tempoArr, targetTempo, marginOfError):
    # TODO define this method as pseudocode


# method to return an array of integers which each represent the tempo in a single measure of the piece.
# audioFile is the mp3/wav file to be analyzed
# beatsPerMeasure is the number of beats in a measure
# tempoEstimate is the tempo the player is aiming to play at.
# Returns an array of integers that represents the tempo of each measure.
def getTempos(audioFile, beatsPerMeasure, tempoEstimate):
    # TODO define this method as pseudocode