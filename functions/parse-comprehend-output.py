import json
import sys

## when calling this function, make sure you pass as a first argument the filename and as a second argument one of these values:
## entities, syntax, sentiment, key_phrases
f = sys.argv[1]
doc_type = sys.argv[2]

with open(f, 'r') as json_file:
    json = json.load(json_file)

if doc_type == 'syntax':
    for loops in json:
        for token in json[loops]["SyntaxTokens"]:
            print('Text: {:<20}\t Syntax: {}'.format(token["Text"], token["PartOfSpeech"]["Tag"]))

elif doc_type == 'sentiment':
    for loops in json:
        print('Overall tone: {}'.format(json[loops]["Sentiment"]))
        for sentiment, score in json[loops]["SentimentScore"].items():
            print('\t{}, Score: {:.2%}'.format(sentiment, score))

elif doc_type == 'entities':
    for loops in json:
        for entity in json[loops]["Entities"]:
            print('Text: {:<30}\tType: {:<10}\tScore: {:.2%}'.format(entity["Text"], entity["Type"], entity["Score"]))

elif doc_type == 'key_phrases':
    for loops in json:
        for phrase in json[loops]["KeyPhrases"]:
            print('Text: {:<30}\tScore: {:.2%}'.format(phrase["Text"], phrase["Score"]))

else:
    print('could not detect which analysis you want printed. Please make sure your second argument is one of those: sentiment, syntax, key_phrases, entities.')


