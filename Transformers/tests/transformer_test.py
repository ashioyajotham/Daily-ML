import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformer import Transformer  
from attention import MultiHeadAttention, softmax

embedding_dim = 300  # GloVe embedding dimension
num_heads = 6  

transformer = Transformer(embedding_dim, num_heads)
sentence = "The quick brown fox"
completed_sentence = transformer.complete_sentence(sentence, temperature=1.0)
print("Completed Sentence:")
print(completed_sentence)