from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import collections

train_set = ["bánh mì ong vàng"]
with open('resources/shop_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        train_set.append(line.lower().strip())
    f.close()

# reverse_index = {}

# for sentense in range(0,10000):
#     arr_word = train_set[sentense].split(' ')
#     for word in arr_word:
#         if word in reverse_index:
#             reverse_index[word].append(sentense)
#         else:
#             reverse_index[word] = [sentense]
# tmp = []
# for word in "bánh mì vợ ông vang".split(' '):
#     tmp = tmp + reverse_index[word]
# recommendation = collections.Counter(tmp).most_common()
# print(train_set[recommendation[0][0]])
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)  #finds the tfidf score with normalization\
tmp_cos = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)[0]
for i in range(len(tmp_cos)):
	if tmp_cos[i] > 0.7:
		print(train_set[i], tmp_cos[i])