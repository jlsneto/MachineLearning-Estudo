import pandas as pd
from ClassCleaner import TextCleaner
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
import os
#import mpld3

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

print('Quantidade de items em vocab_frame: ' + str(vocab_frame.shape[0]))
print(vocab_frame.head())

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features = 20000,
                                   min_df=0.2, stop_words='english',
                                   use_idf=True, tokenizer=tokenize_and_stem,ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(questionTextClean)
terms = tfidf_vectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

from sklearn.cluster import KMeans
num_clusters = 4
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

from sklearn.externals import joblib

#joblib.dump(km, 'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

postsFrame = { 'Title':titleTextClean, 'Question': questionTextClean, 'AnswerAccepted': answerTextClean, 'Cluster': clusters}
frame = pd.DataFrame(postsFrame, index = [clusters], columns = ['Title','Question', 'AnswerAccepted','Cluster'])

order_centroids = km.cluster_centers_.argsort()[:,::-1]

for i in range(num_clusters):
    print("CLUSTER %d Palavras:" %i)

    for ind in order_centroids[i, :6]:
        print(' %s' %vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0],end='\n')
        print()
        print()

    print("CLUSTER %d Text:" %i)
    for question in frame.ix[i]['Question'].values.tolist():
        print(' %s' % question[:40])
    print()
    print()
print("Prediction")

Y = tfidf_vectorizer.transform(["I have a picture gallery where after every three pictures, an ad is displayed gotta pay those bills . So in an example scenario, my gallery would have slides, of which there are pictures and ads, like this In the top row of this drawing are the zerobased indexes of the slides, which I have in an array. What I need to come up with now is a formula to calculate the index of the picture corresponding to a given slide ID the numbers in the bottom row. So for , I need , for , I need and for , the result would be. For a slide that contains an ad, I would like to have the index of the last pic, so for \u2192. I do have a working solution already, where I just use a loop, but this seems really lame and  with a simple math formula, so basically, refactor the above code to avoid the loop and calculate the number through a math formula?"])
prediction = km.predict(Y)
print(prediction)

Y = tfidf_vectorizer.transform(["refactoring"])
prediction = km.predict(Y)
print(prediction)

'''
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.manifold import MDS

MDS()

mds = MDS(n_components=2, dissimilarity="precomputed",random_state=1)

pos = mds.fit_transform(dist)

xs, ys = pos[:, 0], pos[:,1]
print()
print()


cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}

cluster_names = {0: 'way, any, working, following, use',
                 1: 'tried, use, code, refactor',
                 2: 'refactor, want, need, working, like',
                 3: 'use, like, does, refactor, just',
                 4: 'code, use, refactor, following'}

df = pd.DataFrame(dict(x = xs, y=ys, label=clusters, title=titleTextClean))

groups = df.groupby('label')

fig, ax = plt.subplots(figsize=(17,9))
ax.margins(0.05)

for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
            label=cluster_names[name], color=cluster_colors[name],
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis='x',
        which='both',
        bottom='off',
        top='off',
        labelbottom='off')
    ax.tick_params(\
        axis='y',
        which='both',
        left='off',
        top='off',
        labelleft='off')

ax.legend(numpoints=1)

for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'][:10], size=8)

plt.show()

'''
