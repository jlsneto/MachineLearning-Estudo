import pandas as pd
from ClassCleaner import TextCleaner
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
import os
import mpld3

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
    allwords_stemmed = tokenize_and_stem(i)
    totalvocab_stemmed.extend(allwords_stemmed)

    allwords_tokenized = tokenize_only(i)
    totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)

print('there are' + str(vocab_frame.shape[0]) + 'items in vocab_frame')
print(vocab_frame.head())

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features = 200000,
                                   min_df=0.2, stop_words='english',
                                   use_idf=True, tokenizer=tokenize_and_stem,ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(questionTextClean)
terms = tfidf_vectorizer.get_feature_names()

from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

from sklearn.cluster import KMeans
num_clusters = 5
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()

from sklearn.externals import joblib

#joblib.dump(km, 'doc_cluster.pkl')

km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()

postsFrame = { 'Title':titleTextClean, 'Question': questionTextClean, 'AnswerAccepted': answerTextClean, 'Cluster': clusters}
frame = pd.DataFrame(postsFrame, index = [clusters], columns = ['Title','Body', 'AnswerAccepted','Cluster'])

#grouped = frame['Title'].groupby(frame['Cluster'])

#grouped.mean()

order_centroids = km.cluster_centers_.argsort()[:,::-1]

for i in range(num_clusters):
    print("CLUSTER %d words:" %i, end='')

    for ind in order_centroids[i, :6]:
        print(' %s' %vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8','ignore'), end=',')
        print()
        print()

    print("CLUSTER %d titles:" %i, end='')
    for title in frame.ix[i]['Title'].values.tolist():
        print(' %s,' % title, end='')
    print()
    print()
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
