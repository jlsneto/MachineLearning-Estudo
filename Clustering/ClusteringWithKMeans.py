import pandas as pd
from ClassCleaner import TextCleaner
import nltk

posts = pd.read_csv('postsUnico.csv')

questionText = posts['Text']

#answerText = posts['AcceptedAnswerId']

cleaner = TextCleaner()

questionTextClean = [cleaner.filter(text) for text in questionText]


#nltk.download('punkt')
textosQuebrados = [nltk.tokenize.word_tokenize(frase) for frase in questionTextClean]
