import math
import unittest
from typing import List, Optional

import torch
from torch import nn
from torch.nn.init import xavier_uniform_

from vocabulary import Vocabulary
from multi_head_attention import MultiheadAttention
from positional_encodings import SinusoidEncoding

# We are creating an Encoder class that will be used to encode the input sequence.
class TransformerEncoder(nn.Module):
    def __init__(
            self,
            embedding: torch.nn.Embedding,
            hidden_dim: int,
            ff_dim: int,
            num_heads: int,
            num_layers: int,
            dropout_p: float,
    ):
        super().__init__()
        self.embed = embedding
        self.hidden_dim = hidden_dim
        self.positional_encoding = SinusoidEncoding(hidden_dim, max_len=5000)
        self.dropout = nn.Dropout(p = dropout_p)
        self.encoder_blocks = nn.ModuleList([
            EncoderBlock(hidden_dim, ff_dim, num_heads, dropout_p)
            for _ in range(num_layers)
        ])

    def _reset_parameters(self):
        for p in self.parameters():
            if p.dim() > 1:
                xavier_uniform_(p)

    def forward(self, input_ids: torch.Tensor, mask: Optional[torch.BoolTensor] = None) -> torch.Tensor:
        x = self.embed(input_ids) * math.sqrt(self.hidden_dim)
        x = x + self.positional_encoding(x)
        x = self.dropout(x)
        for encoder in self.encoder_blocks:
            x = encoder_block(x, mask = mask)

        return x
    
# We are creating an EncoderBlock class that will be used to encode the input sequence.

class EncoderBlock(nn.Module):
    def __init__(
            self,
            hidden_dim: int,
            ff_dim: int,
            num_heads: int,
            dropout_p: float,
    ):
        super().__init__()
        self.attention = MultiheadAttention(hidden_dim, num_heads)
        self.ff = nn.Sequential(
            nn.Linear(hidden_dim, ff_dim),
            nn.ReLU(),
            nn.Linear(ff_dim, hidden_dim),
        )

        self.dropout1 = nn.Dropout(p = dropout_p)
        self.dropout2 = nn.Dropout(p = dropout_p)
        self.layer_norm1 = nn.LayerNorm(hidden_dim)
        self.layer_norm2 = nn.LayerNorm(hidden_dim)

    def forward(self, x: torch.Tensor, mask: Optional[torch.BoolTensor] = None):
        output = self.dropout1(
            self.attention.forward(x, mask = mask)
        )
        x = self.layer_norm1(x + output)
        output = self.dropout2(
            self.ff(x)
        )
        x = self.layer_norm2(x + output)
        return x
    
class TestEncoder(unittest.TestCase):
    def test_transformer_encoder_single_sequence_batch(self):
        batch = ["Hello my name is Jotham and I was born with the name Jotham"]
        en_vocab = Vocabulary(batch)
        en_vocab_size = len(en_vocab.token_to_index.items())
        with torch.no_grad():
            encoder = TransformerEncoder(
                embedding = torch.nn.Embedding(en_vocab_size, 512)
                hidden_dim = 512,
                ff_dim = 2048,
                num_heads = 8,
                num_layers = 2,
                dropout_p = 0.1
            )
            encoder._reset_parameters()
            encoder.eval()

            input_batch = torch.IntTensor(
                en_vocab.batch_encode(batch, add_special_tokens = False)
            )