import math
import unittest
from typing import List, Optional

import torch
from torch import nn
from torch.nn import functional as F
from utils import construct_future_mask

# We are creating an MultiheadAttention class ie a multi-head attention mechanism which refers to running multiple attention mechanisms in parallel.

class MultiheadAttention(nn.Module):
    def __init__(self, hidden_dim: int, num_heads: int):
        super().__init__()

        assert hidden_dim % num_heads == 0, "hidden_dim must be divisible by num_heads"
        self.qkv_dim = hidden_dim // num_heads
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads

        self.qkv_projection = nn.Linear(hidden_dim, 3 * num_heads * self.qkv_dim, bias=False)
        self.output_projection = nn.Linear(num_heads * self.qkv_dim, hidden_dim, bias=False)
        self._reset_parameters()

    def _reset_parameters(self):
        """Weights initialization"""
        nn.init.xavier_uniform_(self.qkv_projection.weight)
        nn.init.xavier_uniform_(self.output_projection.weight)

    def forward(self, 
                x: torch.Tensor, 
                encoder_hidden_states: Optional[torch.Tensor] = None,
                src_padding_mask: Optional[torch.BoolTensor] = None,
                future_mask: Optional[torch.BoolTensor] = None) -> torch.Tensor:
        """
        Forward pass of the multi-head attention mechanism. Self attention is applied if encoder_hidden_states is None.
        :param x: input tensor of shape (batch_size, seq_len, hidden_dim)
        :param encoder_hidden_states: hidden states of the encoder
        :param src_padding_mask: mask for source sequence
        :param future_mask: mask for future tokens
        :return: output tensor of shape (batch_size, seq_len, hidden_dim)
        """
        batch_size, seq_len, hidden_dim = x.size()

        if encoder_hidden_states is None:
            q, k, v = self._self_attention_projection(x)
        else:
            q, k, v = self._cross_attention_projection(x, encoder_hidden_states)

        # swap dimensions to (batch_size, num_heads, seq_len, qkv_dim)
        q = q.permute(0, 2, 1, 3)
        k = k.permute(0, 2, 1, 3)
        v = v.permute(0, 2, 1, 3)

        # compute the value vector for each head
        values, attn = self.scaled_dot_product_attention(q, k, v, src_padding_mask, future_mask)

        # concatenate the value vectors 
        values = values.reshape(batch_size, seq_len, hidden_dim)

        # apply output projection
        output = self.output_projection(values)
        return output
    
    def _self_attention_projection(self, x: torch.Tensor):
        """
        Project the input tensor to query, key and value tensors.
        :param x: input tensor of shape (batch_size, seq_len, hidden_dim)
        :return: query, key and value tensors
        """
        batch_size, seq_len, _  = x.size()
        qkv = self.qkv_projection(x)
        qkv = qkv.reshape(batch_size, seq_len, self.num_heads, 3 * self.qkv_dim)
        q, k, v = torch.chunk(qkv, 3, dim=-1)
        return q, k, v
    
    def _cross_attention_projection(self, 
                                    encoder_hidden_states: torch.Tensor,
                                    decoder_hidden_states: torch.Tensor):
        """
        Project the input tensor to query, key and value tensors for cross attention.
        :param encoder_hidden_states: hidden states of the encoder
        :param decoder_hidden_states: hidden states of the decoder
        :return: query, key and value tensors
        """
        batch_size, src_seq_len, hidden_dim = encoder_hidden_states.shape
        batch_size, tgt_seq_len, hidden_dim = decoder_hidden_states.shape

        W_q, w_kv = self.qkv_projection.weight.split([hidden_dim, 2 * hidden_dim], dim=0)

        k, v = (F.linear(encoder_hidden_states, weight=w_kv)
                .reshape(batch_size, src_seq_len, self.num_heads, 2*self.qkv_dim)
                .chunk(2, dim=-1))
        
        q = (F.linear(input = decoder_hidden_states, weight=W_q)
                .reshape(batch_size, tgt_seq_len, self.num_heads, self.qkv_dim))
        return q, k, v
    
    def scaled_dot_product_attention(self,
                                     q: torch.Tensor,
                                        k: torch.Tensor,
                                        v: torch.Tensor,
                                        src_padding_mask: Optional[torch.BoolTensor] = None,
                                        future_mask: Optional[torch.BoolTensor] = None):
        """
        Compute the scaled dot-product attention
        :param q: query tensor of shape (batch_size, num_heads, seq_len, qkv_dim)
        :param k: key tensor of shape (batch_size, num_heads, seq_len, qkv_dim)
        :param v: value tensor of shape (batch_size, num_heads, seq_len, qkv_dim)
        :param src_padding_mask: mask for source sequence
        :param future_mask: mask for future tokens
        :return: output tensor of shape (batch_size, seq_len, hidden_dim)
        """
        # compute the scaled dot-product attention
        attn_logits = torch.matmul(q, torch.transpose(k, -1, -2))

        if src_padding_mask is not None or future_mask is not None:
            attn_logits = self.mask_logits(attn_logits, src_padding_mask, future_mask) #type: ignore

        attention = F.softmax(attn_logits, dim=-1)

        # apply attention to the value vectors
        values = torch.matmul(attention, v)
        
        return values, attention
