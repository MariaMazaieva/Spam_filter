

def long_word(array):
    # words = array.split()
    if not array:
        return 
    maximum = max(array, key = len)
    return len(maximum),maximum



if __name__  == "__main__":
    sentence = "kapustr","okkkura","wekofjwejkof"
    # array = ["kapustr","okkkura","wekofjwejkof"]
    long_word(sentence)
    print(long_word(sentence))


