import sys
import re
import methods
import math

if len(sys.argv) != 3:
    sys.exit(0)

training_file = sys.argv[1]
test_file = sys.argv[2]
training_output_name = "preprocessed_train.txt"
test_output_name = "preprocessed_test.txt"
vocabulary = list()
train_sentences = list()
test_sentences = list()

#create vocabulary from training file
with open(training_file, "r") as file:
    for line in file:
        if line:
            #remove punctuation
            line = re.sub(r'[^\w\s]','',line)
            line = line.lower()
            line = line.split()
            #add line to list of sentences including the binary thing at the end
            train_sentences.append(line)
            #add to vocab and remove the number at the end
            for i in range(len(line) - 1):
                if line[i] not in vocabulary:
                    vocabulary.append(line[i])
    file.close()
        
vocabulary = sorted(vocabulary, key=str.lower)


#load test file
with open(test_file, "r") as file:
    for line in file:
        if line:
            #remove punctuation
            line = re.sub(r'[^\w\s]','',line)
            line = line.split()
            #add line to list of sentences including the binary thing at the end
            test_sentences.append(line)
    file.close()

train_features = methods.preprocess_sentences(vocabulary, train_sentences)
test_features = methods.preprocess_sentences(vocabulary, test_sentences)

methods.write_to_file(vocabulary, train_features,  training_output_name)
methods.write_to_file(vocabulary, test_features,  test_output_name)


#probabilities[i][j] where i is the probability of a feature being true given j
probabilities = [[0]*2 for _ in range(len(train_features[0]) - 1)]
sum_all_cases = len(train_features)
prob_pos = 0

#calculate the probabilities of all words given the review is positive or negative
for col in range(len(train_features[0]) - 1):
    sum_pos_given_pos = 0
    sum_pos_cases = 0
    sum_pos_given_neg = 0
    for row in range(len(train_features)):
        if train_features[row][-1]:
            sum_pos_cases += 1
            if train_features[row][col]:
                sum_pos_given_pos += 1
        elif train_features[row][col]:
            sum_pos_given_neg += 1

    prob_pos = sum_pos_cases/sum_all_cases
    sum_neg_cases = sum_all_cases - sum_pos_cases 
    #probabilities[col][1] = math.log((sum_pos_given_pos + 1)/(sum_pos_cases + 2), 10)
    #probabilities[col][0] = math.log((sum_pos_given_neg + 1)/(sum_neg_cases + 2), 10)
    probabilities[col][1] = (sum_pos_given_pos + 1)/(sum_pos_cases + 2)
    probabilities[col][0] = (sum_pos_given_neg + 1)/(sum_neg_cases + 2)



correct_predictions = 0
for i in range(len(test_features)):
    prob_pos_case = 0
    prob_neg_case = 0
    for j in range(len(test_features[i]) - 1):
        if test_features[i][j]:
            prob_pos_case += math.log(probabilities[j][1],10)
            prob_neg_case += math.log(probabilities[j][0],10)
        else:
            prob_pos_case += math.log((1 - probabilities[j][1]),10) 
            prob_neg_case += math.log((1 - probabilities[j][0]),10)
    prediction_pos = prob_pos_case + math.log(prob_pos, 10)
    prediction_neg = prob_neg_case + math.log(1-prob_pos, 10)
    #prediction_pos = math.log(prob_pos_case,10) + math.log(prob_pos, 10)
    #prediction_neg = math.log(prob_neg_case,10) + math.log(1-prob_pos, 10)
    prediction = 0
    if prediction_pos > prediction_neg:
        prediction = 1
    if prediction == test_features[i][-1]:
        correct_predictions += 1
print((correct_predictions/sum_all_cases)*100, '%')
    