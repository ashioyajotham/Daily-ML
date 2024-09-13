import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # for importing from parent directory

from transformer import Transformer
from attention import MultiHeadAttention, softmax

embedding_dim = 300  # GloVe embedding dimension
num_heads = 6 # Number of attention heads

transformer = Transformer(embedding_dim, num_heads)
sentence = "this is a test"
completed_sentence = transformer.complete_sentence(sentence, temperature=1.0)
print("Completed Sentence:")
print(completed_sentence)