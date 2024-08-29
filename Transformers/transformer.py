import numpy as np
from embed import tokenize_and_embed, add_positional_encoding, embedding_model
from attention import MultiHeadAttention, softmax

class Transformer:
    def __init__(self, embedding_dim, num_heads):
        """
        Initialize the Transformer model
        Args:
            embedding_dim(int): Embedding dimension
            num_heads(int): Number of attention heads
        """
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.multi_head_attention = MultiHeadAttention(embedding_dim, num_heads)
        self.output_projection = self.output_projection * np.sqrt(1./embedding_dim) # scale the values down by the square root of the embedding dimension

    def forward(self, embeddings):
            
        # Add positional encoding to the embeddings
        embeddings_with_pos = add_positional_encoding(embeddings)
        
        # Apply multi-head attention mechanism
        attention_output = self.multi_head_attention.forward(embeddings_with_pos)
        
        # Apply the output weight matrix
        output = self.linear_transform(attention_output, self.output_projection)
        return output
    
    # calculate linear transformation
    def linear_transformation(self, x, weight_matrix):
        """
        Apply linear transformation to the input
        Args:
            x(np.ndarray): Input to be transformed
            weight_matrix(np.ndarray): Weight matrix for output
        Returns:
            np.ndarray: Output after applying linear transformation
        """
        return np.dot(x, weight_matrix)
    
    # calculate the next token
    def predict_next_word(self, sentence, temperature, top_k=5):
        # Tokenize and embed the input sentence
        embeddings = tokenize_and_embed(sentence, embedding_model)
        output = self.forward(embeddings)

        # Apply softmax to the output to get probabilities
        probs = softmax(output[-1]/temperature)

        # sample from the top_k words instead of greedy decoding
        top_k_indices = np.argsort(probs)[-top_k:]
        chosen_index = np.random.choice(top_k_indices)
        next_word = embedding_model.index_to_key[chosen_index]

        return next_word
    
    # complete the sentence from the given input
    def complete_sentence(self, sentence, max_length = 20, temperature = 1.0):
        words = sentence.split()

        for _ in range(max_length - len(words)):
            next_word = self.predict_next_word("". join(words), temperature)
            if next_word == "<EOS>":
                break
            words.append(next_word)
            return " ".join(words)
        
        # Initialize the Transformer model
transformer = Transformer(embedding_dim=300, num_heads=5)

# Complete the sentence
sentence = "The cat"
completed_sentence = transformer.complete_sentence(sentence)
print(completed_sentence)

# To run the code, you need to have the following files in the same directory as the code:
#     1. Transformers/attention.py
#     2. Transformers/embed.py
#     3. Transformers/transformer.py

# The code defines a Transformer class that uses the MultiHeadAttention mechanism to predict the next word in a sentence. The Transformer class has the following methods:
#     1. __init__: Initializes the Transformer model with the embedding dimension and the number of attention heads.
#     2. forward: Applies the multi-head attention mechanism to the input embeddings and returns the output
#     3. linear_transformation: Applies a linear transformation to the input using a weight matrix
#     4. predict_next_word: Predicts the next word in a sentence using the Transformer model
#     5. complete_sentence: Completes the sentence by predicting the next word until the end of the sentence token is reached

# The code then creates an instance of the Transformer class and uses it to complete a sentence starting with "The cat".

# To run the code, save the code snippet in a file named transformer.py in the Transformers directory. Make sure to have the attention.py and embed.py files in the same directory.

# Then go on the terminal and run the following command:
#     python transformer.py
