sentence = "The cat sat on the mat"

tokens = sentence.lower().split()

print("Sentence:", sentence)

print("Tokens  :", tokens)

vocab = {word: idx for idx, word in enumerate(set(tokens))}

token_ids = [vocab[t] for t in tokens]

print("Vocabulary:", vocab)

print("Token IDs :", token_ids)

import numpy as np



np.random.seed(42)

EMBED_DIM = 4



embedding_table = {word: np.random.randn(EMBED_DIM) for word in vocab}



print("Embeddings for each token:\n")

for token in tokens:

 vec = embedding_table[token]

print(f"  {token:<6} → {vec.round(2)}")

def cosine_similarity(v1, v2):

 return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))



word_vecs = {

"cat": np.array([0.9, 0.1, 0.2, 0.0]),

"dog": np.array([0.8, 0.2, 0.2, 0.0]),
"mat": np.array([0.1, 0.9, 0.1, 0.0]),

"sat": np.array([0.1, 0.8, 0.2, 0.0]),

"king": np.array([0.0, 0.1, 0.9, 0.8]),

}



pairs = [("cat", "dog"), ("cat", "king"), ("mat", "sat")]



print("Cosine Similarity:\n")

for w1, w2 in pairs:

 sim = cosine_similarity(word_vecs[w1], word_vecs[w2])

print(f" {w1} ↔️ {w2} → {sim:.2f}")

import matplotlib.pyplot as plt


words = list(word_vecs.keys())

x = [word_vecs[w][0] for w in words]

y = [word_vecs[w][1] for w in words]


plt.figure(figsize=(6, 5))

plt.scatter(x, y, color='steelblue', s=200)


for i, word in enumerate(words):

 plt.annotate(word, (x[i], y[i]),

   textcoords='offset points',
   xytext=(8, 5), fontsize=13)


plt.title("Word Embeddings — 2D View")

plt.xlabel("Dimension 1")

plt.ylabel("Dimension 2")

plt.grid(True, linestyle='--', alpha=0.5)

plt.show()


print("cat & dog are close → similar meaning!")

print("king is far away   → different meaning!")



def cosine_similarity(v1, v2):

 return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))



word_vecs = {

 "cat": np.array([0.9, 0.1, 0.2, 0.0]),

 "dog": np.array([0.8, 0.2, 0.2, 0.0]),

 "mat": np.array([0.1, 0.9, 0.1, 0.0]),

 "sat": np.array([0.1, 0.8, 0.2, 0.0]),

 "king": np.array([0.0, 0.1, 0.9, 0.8]),

}



pairs = [("cat", "dog"), ("cat", "king"), ("mat", "sat")]
