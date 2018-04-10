import pandas as pd
from ClassCleaner import TextCleaner
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
import os

posts = pd.read_csv('PostBody.csv')

titleQuestionText = posts['Title']
questionText = posts['Body']

answerText = posts['AnswerAccepted']


cleaner = TextCleaner()

titleTextClean = [cleaner.filter(title) for title in titleQuestionText]
questionTextClean = [cleaner.filter(question) for question in questionText]
answerTextClean = [cleaner.filter(answer) for answer in answerText]


#nltk.download('punkt')
#questionSplitText = [nltk.tokenize.word_tokenize(frase) for frase in questionTextClean]
stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer('english')

#tokenizer e o stemmer
def tokenize_and_stem(text):
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []

    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]',token):
            filtered_tokens.append(token)
    return filtered_tokens

totalvocab_stemmed = []
totalvocab_tokenized = []

for i in questionTextClean:
    todas_palavras_stemmed = tokenize_and_stem(i)
    totalvocab_stemmed.extend(todas_palavras_stemmed)

    todas_palavras_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(todas_palavras_tokenized)

vocab_frame = pd.DataFrame({'palavras': totalvocab_tokenized}, index = totalvocab_stemmed)

from nltk import FreqDist
#Conta e plota a quantidade de vezes que a palavra apareceu no vocabulário
fdist = FreqDist(totalvocab_tokenized)
fdist.plot(50, cumulative = True)

#verifica as palavras que sejam entre 8 e 13 caracters e que tenham ocorrido mais de 5 vezes
longas = sorted([w for w in totalvocab_tokenized if len(w) in range(8,13) and fdist[w] >= 7])
#plotagem do de longas
fdistTratada = FreqDist(longas)
fdistTratada.plot(50, cumulative = True)

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features = 20000,
                                   min_df=0.2, stop_words='english',
                                   use_idf=True, tokenizer=tokenize_and_stem,ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(questionTextClean)
#verificar os termos...
terms = tfidf_vectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

from sklearn.cluster import KMeans
num_clusters = 4
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

from sklearn.externals import joblib

#Persistencia de model
try:
    km = joblib.load('persist_model.pkl')
except:
    joblib.dump(km, 'persist_model.pkl')

clusters = km.labels_.tolist()

postsFrame = { 'Title':titleTextClean, 'Question': questionTextClean, 'AnswerAccepted': answerTextClean}
frame = pd.DataFrame(postsFrame, index = [clusters], columns = ['Title','Question', 'AnswerAccepted'])

order_centroids = km.cluster_centers_.argsort()[:,::-1]

for i in range(num_clusters):
    print('\n')
    print('CLUSTER %d:' %i)

    for ind in order_centroids[i, :6]:
        print(' %s' %vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0],end='|')
        
    print('\n')
    
    for question in frame.ix[i]['Title'].values.tolist():
        print(' %s' % question, end='\n')

print('\n')
print('\n')
print("Prediction")

Y = tfidf_vectorizer.transform(["I have a picture gallery where after every three pictures, an ad is displayed gotta pay those bills . So in an example scenario, my gallery would have slides, of which there are pictures and ads, like this In the top row of this drawing are the zerobased indexes of the slides, which I have in an array. What I need to come up with now is a formula to calculate the index of the picture corresponding to a given slide ID the numbers in the bottom row. So for , I need , for , I need and for , the result would be. For a slide that contains an ad, I would like to have the index of the last pic, so for \u2192. I do have a working solution already, where I just use a loop, but this seems really lame and  with a simple math formula, so basically, refactor the above code to avoid the loop and calculate the number through a math formula?"])
prediction = km.predict(Y)
print(prediction)

Y = tfidf_vectorizer.transform(["Your formula is almost correct, you only have to add to the slide index and ad interval to fix it"])
prediction = km.predict(Y)
print(prediction)
