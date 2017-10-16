# This file contains the backend methods that will process the output of Essentia and provide understandable feedback based on this.

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
                steadyDuration++
        elif (fastDuration > 0):
            # The last measure(s) was fast
            if (tempoArr[measure] > (targetTempo + marginOfError)):
                # This measure is fast
                fastDuration++
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
            elif (tempoArr[measure] < (targetTemp - marginOfError)):
                # This measure is slow
                slowDuration++
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
    if (behaviorList[0][0] == "slow"):
        description = "You started out slow, and were slow for " + str(behaviorList[0][1]) + " measures until measure number " + str(behaviorList[0][2]) + ".\n"
    elif (behaviorList[0][0] == "fast"):
        description = "You started out fast, and were fast for " + str(behaviorList[0][1]) + " measures until measure number " + str(behaviorList[0][2]) + ".\n"
    elif (behaviorList[0][0] == "steady"):
        description = "You started our steady, and were steady for " + str(behaviorList[0][1]) + " measures until measure number " + str(behaviorList[0][2]) + ".\n"
    # Create the description for the second line throgh the second to last line
    for index in  range(1, len(behaviorList) - 1):
        if (behaviorList[index][0] == "slow"):
            description += "Starting in measure " + str(behaviorList[index - 1][2] + 1) + " you were slow, and were slow for " + str(behaviorList[index][1]) + " measures until measure number " + str(behaviorList[index][2]) + ".\n"
        elif (behaviorList[index][0] == "fast"):
            description += "Starting in measure " + str(behaviorList[index - 1][2] + 1) + " you were fast, and were fast for " + str(behaviorList[index][1]) + " measures until measure number " + str(behaviorList[index][2]) + ".\n"
        elif (behaviorList[index][0] == "steady"):
            description += "Starting in measure " + str(behaviorList[index - 1][2] + 1) + " you were steady, and were steady for " + str(behaviorList[index][1]) + " measures until measure number " + str(behaviorList[index][2]) + ".\n"
    # Create the description of the final line
    if (behaviorList[len(behaviorList) - 1][0] == "slow"):
        description += "Starting in measure " + str(behaviorList[len(behaviorList) - 2][2] + 1) + " you were slow, and were slow for " + str(behaviorList[len(behaviorList) - 1][1]) + " measures until the end of the piece.\n"
    elif (behaviorList[len(behaviorList) - 1][0] == "fast"):
        description += "Starting in measure " + str(behaviorList[len(behaviorList) - 2][2] + 1) + " you were fast, and were fast for " + str(behaviorList[len(behaviorList) - 1][1]) + " measures until the end of the piece.\n"
    elif (behaviorList[len(behaviorList) - 1][0] == "steady"):
        description += "Starting in measure " + str(behaviorList[len(behaviorList) - 2][2] + 1) + " you were steady, and were steady for " + str(behaviorList[len(behaviorList) - 1][1]) + " measures until the end of the piece.\n"
    # Return this string
    return description


# method to return an array of integers which each represent the tempo in a single measure of the piece.
# audioFile is the mp3/wav file to be analyzed
# beatsPerMeasure is the number of beats in a measure
# tempoEstimate is the tempo the player is aiming to play at.
# Returns an array of integers that represents the tempo of each measure.
def getTempos(audioFile, beatsPerMeasure, tempoEstimate):
    # TODO define this method as pseudocode