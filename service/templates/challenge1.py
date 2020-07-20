# challenge 1  : Algorithm test

def compress(input_string):
    word_track = {}
    for i in input_string:
        if(i not in word_track.keys()):
            word_track[i] = 1
        else:
            word_track[i] = word_track[i] + 1
    output_string = ""
    for i in word_track.keys():
        print(i)
        if(word_track[i] != 1):
            output_string = output_string + i + str(word_track[i])
        else:
            output_string = output_string + i
    return output_string


print(compress("aaabbcc"))
