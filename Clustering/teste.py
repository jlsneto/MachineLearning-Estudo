import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import nltk
from ClassCleaner import TextCleaner

posts = pd.read_csv('PostBody.csv')

questionText = posts['Title']

#answerText = posts['AcceptedAnswerId']

cleaner = TextCleaner()

documents = [cleaner.filter(text).lower() for text in questionText]

#documents = [nltk.tokenize.word_tokenize(frase) for frase in documentsCleaner]

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)


qtd_clusters = 3
model = KMeans(n_clusters=qtd_clusters, init='k-means++', n_init=1)
model.fit(X)

print("Principais termos por Cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(qtd_clusters):
    print(i)
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print()


print("\n")
print("Prediction")

Y = vectorizer.transform(["I have a picture gallery where after every three pictures, an ad is displayed gotta pay those bills \U0001f600. So in an example scenario, my gallery would have slides, of which there are pictures and ads, like this In the top row of this drawing are the zerobased indexes of the slides, which I have in an array. What I need to come up with now is a formula to calculate the index of the picture corresponding to a given slide ID the numbers in the bottom row. So for , I need , for , I need and for , the result would be. For a slide that contains an ad, I would like to have the index of the last pic, so for \u2192. I do have a working solution already, where I just use a loop, but this seems really lame and cumbersome I'm sure there is a much more elegant solution with a simple math formula, so basically, it's more a math question than a JavaScript question How can I refactor the above code to avoid the loop and calculate the number through a math formula? I have tried something like this But that gives me incorrect values which are more and more off as slide index increases. See JSFiddle"])
prediction = model.predict(Y)
print(prediction)

Y = vectorizer.transform([" I have a picture gallery where after every three pictures, an ad is displayed gotta pay those bills \U0001f600. So in an example scenario, my gallery would have slides, of which there are pictures and ads, like this In the top row of this drawing are the zerobased indexes of the slides, which I have in an array. What I need to come up with now is a formula to calculate the index of the picture corresponding to a given slide ID the numbers in the bottom row. So for , I need , for , I need and for , the result would be. For a slide that contains an ad, I would like to have the index of the last pic, so for \u2192. I do have a working solution already, where I just use a loop, but this seems really lame and cumbersome I'm sure there is a much more elegant solution with a simple math formula, so basically, it's more a math question than a JavaScript question How can I refactor the above code to avoid the loop and calculate the number through a math formula? I have tried something like this But that gives me incorrect values which are more and more off as slide index increases. See JSFiddle"])
prediction = model.predict(Y)
print(prediction)
