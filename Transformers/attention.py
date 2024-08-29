import numpy as np
import torch
import os
from embed import get_embedding

def softmax(scores):
    """
    Apply softmax to normalize attention scores

    Args:
    scores(np.ndarray): Attention scores

    Returns:
    np.ndarray: Normalized attention scores
    """
    exp_scores = np.exp(scores, axis = 1, keepdims = True) # numerical stability and normalizes across each row (ie across all key vectors for each query vector)
    # keepdims = True to keep the dimension of the original array so that we can broadcast it
    return exp_scores / np.sum(exp_scores)

class SelfAttention: # It is the layer that computes the attention scores between the query and key vectors and then applies the attention scores to the value vectors to get the output
    """
    Self Attention mechanism to compute attention scores
    Attributes:
    embed_dim(int): Embedding dimension
    W_q(np.ndarray): Weight matrix for query # query is the vector that we want to compare to all the keys
    W_k(np.ndarray): Weight matrix for key # key is the vector that we want to compare to the query
    W_v(np.ndarray): Weight matrix for value # value is the vector that we want to output
    """

    def __init__(self, embedding_dim):
        """
        Initialize the SelfAttention mechanism
        Args:
            embed_dim(int): Embedding dimension
        """
        self.embedding_dim = embedding_dim

        # Initialize the weight matrices with small random numbers from a normal distribution
        self.W_q = np.random.randn(embedding_dim, embedding_dim) * np.sqrt(1. / embedding_dim)
        self.W_k = np.random.randn(embedding_dim, embedding_dim) * np.sqrt(1. / embedding_dim)
        self.W_v = np.random.randn(embedding_dim, embedding_dim) * np.sqrt(1. / embedding_dim)

    def forward(self, emdeddings, mask = None):
        """
        Forward pass through the self attention mechanism to compute attention scores
        Args:
            embeddings(np.ndarray): Input embeddings
            mask(np.ndarray, optional): Mask to be applied to the attention scores to avoid attending to certain elements
        Returns:
            np.ndarray: Attention scores (output after applying attention scores to the values)
        """
        query = np.dot(emdeddings, self.W_q)
        key = np.dot(emdeddings, self.W_k)
        values = np.dot(emdeddings, self.W_v)

        # Compute the attention scores
        attention_scores = np.calculate_attention_scores(query, key)

        # Masking
        if mask is not None:
            attention_scores = np.where(mask==0, -1e9, attention_scores) # if mask is 0, then set the attention score to -1e9
            # if mask is 1, then keep the attention score as it is

        # Apply softmax to normalize the attention scores
        attention_weights = softmax(attention_scores)
        output = self.values_weighted_sum(values, attention_weights)
        return output
    
    def calculate_attention_score(self, query, key):
        """
        Calculate attention scores based on the query and key matrices
        Args:
            query(np.ndarray): Query matrix
            key(np.ndarray): Key matrix
        Returns:
            np.ndarray: Attention scores
        """
        d_k = query.shape[-1] # scaling factor to ensure that not too large values are fed to the softmax function as it would result in numerical instability 
                            # (would push softmax into regions where the gradients are very small)
        dot = np.dot(query, key.T) # key.T is the transpose of the key matrix
                                # flipping the matrix over its diagonal,such that the row and column indices are switched
        return dot / np.sqrt(d_k) # scale by the square root of the key dimension
    
    def values_weighted_sum(self, weights, values):
        """
        Weighted sum of values based on the attention weights
        Args:
            weights(np.ndarray): Attention weights
            values(np.ndarray): Values to be weighted
        Returns:
            np.ndarray: Weighted sum of values
        """
        return np.dot(weights, values)
    
class MultiHeadAttention: # It is the layer that splits the input embeddings into multiple heads, applies the self attention mechanism to each head, concatenates the heads, and applies the output weight matrix to get the output
    """
    Multi-head attention mechanism consisting of multiple self attention heads
    Attributes:
    head_dim(int): Dimension of each attention head
    attention_heads(list): list of self attention heads
    W_o(np.ndarray): Weight matrix for output
    """

    def __init__(self, embedding_dim, num_heads):
        """
        Initialize the MultiHeadAttention mechanism
        Args:
            embed_dim(int): Embedding dimension
            num_heads(int): Number of attention heads
        
        Raises:
            ValueError: If the embedding dimension is not divisible by the number of heads
        """
        # embedding_dim must be divisible by num_heads
        # otherwise, the context window will be different for each head ie inconsistent context window
        if embedding_dim % num_heads != 0:
            raise ValueError("Embedding dimension must be divisible by the number of heads")
        
        # compute the dimension of each head
        self.head_dim = embedding_dim // num_heads

        # Initialize the attention heads (instances of the SelfAttention class)
        self.attention_heads = [SelfAttention(self.head_dim) for _ in range(num_heads)]

        # Initialize the output weight matrix
        self.W_o = np.random.randn(embedding_dim, embedding_dim)

    def forward(self, embeddings):
        """
        Forward pass through the multi-head attention mechanism to compute attention scores
        Args:
            embeddings(np.ndarray): Input embeddings

        Returns:
            np.ndarray: Attention scores (output after applying attention scores to the values)
        """
        # Split the embeddings into multiple heads
        sequence_length, embedding_dim = embeddings.shape
        split_embeddings = np.reshape(embeddings, (sequence_length, -1, self.head_dim))

        head_outputs = []
        for i, head in enumerate(self.attention_heads):
            head_output = head.forward[:, i, :]
            head_outputs.append(head_output)

        # Concatenate the heads
        concatenated_output = np.concatenate(head_outputs, axis = -1)

        # Apply the output weight matrix
        output = self.linear_transform(concatenated_output, self.W_o)

        return output

    def linear_transformation(self, concatenated_output, weight_matrix):
        """
        Apply linear transformation to the concatenated output
        Args:
            concatenated_output(np.ndarray): Concatenated output of the attention heads
            weight_matrix(np.ndarray): Weight matrix for output
        Returns:
            np.ndarray: Output after applying the linear transformation
        """
        return np.dot(concatenated_output, weight_matrix)