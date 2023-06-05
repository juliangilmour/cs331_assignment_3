def preprocess_sentences(vocabulary, sentences):
    features = [[0]*(len(vocabulary) + 1) for _ in range(len(sentences))] 
    word = 0
    for i in range(len(sentences)):
        for j in range(len(sentences[i]) - 1):
            if sentences[i][j] in vocabulary:
                word = vocabulary.index(sentences[i][j])
                features[i][word] = 1
        if sentences[i][-1] == '1':
            features[i][-1] = 1
        else:
            features[i][-1] = 0

    return features

def write_to_file(vocabulary, features, name):
    file = open(name, "w")
    line = ""

    for i in range(len(vocabulary)):
        line += vocabulary[i]
        line += ','
    line += "classlabel\n"
    file.write(line)

    for i in range(len(features) - 1):
        line = ""
        for j in range(len(features[i])):
            line += str(features[i][j])
            line += ','
        line = line[:-1]
        line += '\n'
        file.write(line)