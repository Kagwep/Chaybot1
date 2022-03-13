from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ListTrainer

# we create the questions from the video tutorial.
"""" We will first create a function that creates questions from the tutorial video.
nltk library helps us create the questions
"""
import nltk

# file name - the genarated script from the tutorial
# note - 'try.txt' is a dumy script
scriptName = 'try.txt'

#script opened
def readFile(scriptName):
    paragraph = ''
    file = open(scriptName, "r")
    paragraph = file.read()
    file.close()
    return paragraph
#tokenizaton of the script
def tokenization(paragraph):
    sents = nltk.sent_tokenize(paragraph)
    words = [nltk.word_tokenize(sent) for sent in sents]
    return sents, words
# parts of speech  tagging, helps in creating the questions.
def posTagging(words):
    posWords = [nltk.pos_tag(word) for word in words]
    return posWords

# get script
paragraph = readFile(scriptName)
#print (paragraph)

# tokenize
sents, words = tokenization(paragraph)

# pos tagging
posWords = posTagging(words)

# question generated bank to help train the bot
questions = []

i = 0
#list to store the all the answers to questions
answers = []

queries = sents

# Replace Nouns with '____'
for posWord in posWords:
    ans = []
    for x in posWord:
        
        if (x[1] == 'NN'):
    
            queries[i] = queries[i].replace(x[0], '__________')
            ans.append(x[0])
            answers.append(x[0])
    #print(ans)
            
    i = i + 1
#queries
i = 1
for query in queries:
    query = (query)
    questions.append(query)
    #print(answers)
    #print ('\n')

    i = i + 1
#print(questions)

""" questions gotten from the video script will be used to train the bot"""

#bot name
elena = ChatBot('elena')

# bot trainer
trainer = ListTrainer(elena)

trainer.train(questions)
print('Hi, my name is Elena. hope you had a good lesson.\n')
print('Here are some questions to test your understanding are you ready?\n')


while True:
    request=input('you :')
    if request == 'OK' or request == 'ok':
        print('Elena: bye')
        break
    else:
        print('Fill in the blanks')
        response=elena.get_response(request)
        print('Elena:', response)
