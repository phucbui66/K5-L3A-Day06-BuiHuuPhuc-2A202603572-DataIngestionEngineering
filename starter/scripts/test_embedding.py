
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

texts = [
    "Python uses the if statement for conditional execution.",
    "The if statement allows conditional branching in Python.",
    "A list is a mutable sequence of Python objects.",
]

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    normalize_embeddings=True,
)

print("Number of texts:", len(texts))
print("Embedding shape:", embeddings.shape)

# Cosine similarity because vectors are normalized
similarity = embeddings @ embeddings.T

print("\nCosine similarity matrix:")
print(np.round(similarity, 3))

assert embeddings.shape == (3, 384)

print("\nPASS: Embedding model works correctly")
