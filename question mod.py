from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ListTrainer
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import ast

""" In this modeule we get the video transcript of the tutoial video"""
# the saved file of the converted video

import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

questions_text = []

num_seconds_video= 52*60
print("The video is {} seconds".format(num_seconds_video))
l=list(range(0,num_seconds_video+1,60))

diz={}
for i in range(len(l)-1):
    ffmpeg_extract_subclip("python.mp4", l[i]-2*(l[i]!=0), l[i+1], targetname="cut{}.mp4".format(i+1))
    clip = mp.VideoFileClip(r"cut{}.mp4".format(i+1)) 
    clip.audio.write_audiofile(r"converted{}.wav".format(i+1))
    r = sr.Recognizer()
    audio = sr.AudioFile("converted{}.wav".format(i+1))
    with audio as source:
      r.adjust_for_ambient_noise(source)  
      audio_file = r.record(source)
    result = r.recognize_google(audio_file)
    diz['chunk{}'.format(i+1)]=result
    l_chunks=[diz['chunk{}'.format(i+1)] for i in range(len(diz))]
    text='\n'.join(l_chunks)
    with open('tutorial_script.txt', 'r') as f:
        n_data = f.readlines()
        for element in l_chunks:
            texts = element.strip('"')
        n_data.append(texts)
        n_data1 = []
        for words in n_data:
            n_data1.append(words.strip())
    with open("tutorial_script.txt", "w") as f:
        f.writelines('.\n'.join(n_data1))
    


# we create the questions from the video tutorial.
"""" We will first create a function that creates questions from the tutorial video.
nltk library helps us create the questions
"""
import nltk

# file name - the genarated script from the tutorial
# note - 'try.txt' is a dumy script
scriptName = 'tutorial_script'

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
