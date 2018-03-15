import pandas as pd
from ClassCleaner import TextCleaner
import nltk

posts = pd.read_csv('posts.csv')

questionText = posts['Text']

answerText = posts['AnswerAccepted']

cleaner = TextCleaner()

questionTextClean = [cleaner.filter(text) for text in questionText]


#nltk.download('punkt')
textosQuebrados = [nltk.tokenize.word_tokenize(frase) for frase in questionTextClean]
