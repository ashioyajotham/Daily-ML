import math
import unittest
from typing import List, Optional
import random
import numpy as np
import torch
from torch import nn
from torch.nn.init import xavier_uniform_
from multi_head_attention import MultiheadAttention
from positional_encodings import SinusoidEncoding
from utils import construct_future_mask

class TransformerDecoder(nn.Module):
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
        self.decoder_blocks = nn.ModuleList([
            TransformerDecoderBlock(hidden_dim, ff_dim, num_heads, dropout_p)
            for _ in range(num_layers)
        ])


    def _reset_parameters(self):
        for p in self.parameters():
            if p.dim() > 1:
                xavier_uniform_(p)

    def forward(
            self,
            x: torch.Tensor,
            encoder_hidden_states: torch.FloatTensor,
            src_mask: Optional[torch.BoolTensor] = None,
            tgt_mask: Optional[torch.BoolTensor] = None,
    ):  
        # Embedding
        output = self.dropout1(self.self_mha.forward(x, tgt_mask = tgt_mask))
        x = self.layer_norm1(x + output)

        # Encoder-Decoder Attention
        output = self.dropout2(self.src_mha.forward(x, encoder_hidden_states, src_mask = src_mask))
        x = self.layer_norm2(x + output)

        # Feed Forward
        output = self.dropout3(self.ff.forward(x))
        x = self.layer_norm3(x + output)

        return x
    
class TransformerDecoderBlock(nn.Module):
    def __init__(self, hidden_dim: int, ff_dim: int, num_heads: int, dropout_p: float):
        super().__init__()

        self.cross_mha = MultiheadAttention(hidden_dim, num_heads)
        self.self_mha = MultiheadAttention(hidden_dim, num_heads)
        self.feed_forward = nn.Sequential(
            nn.Linear(hidden_dim, ff_dim), nn.ReLU(), nn.Linear(ff_dim, hidden_dim),
        )

        self.dropout1 = nn.Dropout(p = dropout_p)
        self.dropout2 = nn.Dropout(p = dropout_p)
        self.dropout3 = nn.Dropout(p = dropout_p)

        self.layer_norm1 = nn.LayerNorm(hidden_dim)
        self.layer_norm2 = nn.LayerNorm(hidden_dim)
        self.layer_norm3 = nn.LayerNorm(hidden_dim)

    def forward(
            self,
            x: torch.Tensor,
            encoder_hidden_states: torch.FloatTensor,
            src_padding_mask: Optional[torch.BoolTensor] = None,
            future_mask: Optional[torch.BoolTensor] = None,
    ):
        output = self.dropout1(self.self_mha.forward(x, future_mask=future_mask))
        x = self.layer_norm1(x + output)

        output = self.dropout2(
            self.cross_mha.forward(
                x,
                encoder_hidden_states = encoder_hidden_states,
                src_padding_mask = src_padding_mask,
            )
        )
        x = self.layer_norm2(x + output)

        output = self.dropout3(self.feed_forward(x))
        x = self.layer_norm3(x + output)
        return x
    
class TestTransformerDecoder(unittest.TestCase):
    def test_one_layer_transformer_decoder_inference(self):
        seed = 0
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

        with torch.no_grad():
            batch_size = 2
            src_seq_len = 10
            hidden_dim = 512
            vocab_size = 2000
            num_heads = 8
            num_layers = 1

            encoder_output = torch.randn(batch_size, src_seq_len, hidden_dim)
            src_padding_mask = torch.BoolTensor(
                [[1, 1, 1, 1, 1, 1, 1, 1, 0, 0]], [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
            )
            tgt_padding_mask = torch.BoolTensor(
                [[1, 1, 1, 1, 1, 1, 1, 1, 0, 0]], [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
            )

            decoder = TransformerDecoder(
                embedding = torch.nn.Embedding(vocab_size, hidden_dim),
                hidden_dim = hidden_dim,
                ff_dim = 2048,
                num_heads = num_heads,
                num_layers = num_layers,
                dropout_p = 0.1,
                vocab_size = vocab_size,
                tie_output_to_embedding = True,
            )
            decoder._reset_parameters()
            decoder.eval()

            bos_token_id = 1
            decoder_input = torch.IntTensor([[bos_token_id], [bos_token_id]])
            tgt_mask = None
            for i in range(3):
                decoder_output = decoder.forward(
                    decoder_input,
                    encoder_output,
                    src_mask = src_padding_mask,
                    tgt_mask = tgt_mask,
                )
                predicted_tokens = torch.argmax(decoder_output[:, -1, :], dim = -1).unsqueeze(-1)
                decoder_input = torch.cat([decoder_input, predicted_tokens], dim = -1)
                tgt_mask = construct_future_mask(decoder_input.shape(1))

                self.assertEqual(decoder_output.shape, (batch_size, i + 1, hidden_dim))
                self.assertEqual(torch.any(decoder_output == 1), False)
                self.assertEqual(torch.all(decoder_input == bos_token_id), True)

    
    def multi_layer_transformer_decoder_inference(self):
        seed = 0
        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

        with torch.no_grad():
            batch_size = 2
            src_seq_len = 10
            hidden_dim = 512
            vocab_size = 2000

            encoder_output = torch.randn((batch_size, src_seq_len, hidden_dim))
            src_padding_mask = torch.BoolTensor(
                [[1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
            )

            decoder = TransformerDecoder(
                embedding = torch.nn.Embedding(vocab_size, hidden_dim),
                hidden_dim = hidden_dim,
                ff_dim = 2048,
                num_heads = 8,
                num_layers = 6,
                dropout_p = .1,
                vocab_size = vocab_size,
                tie_output_to_embedding = False
            )
            decoder._reset_parameters()
            decoder.eval()

            bos_token_id = 10
            decoder_input = torch.IntTensor([[bos_token_id], [bos_token_id]])
            tgt_mask = None
            for i in range(3):
                decoder_output = decoder(
                    decoder_input,
                    encoder_output,
                    src_padding_mask = src_padding_mask,
                    tgt_mask = tgt_mask,
                )
                predicted_tokens = torch.argmax(
                    decoder_output[:, -1, :], dim = -1
                ).unsqueeze(1)
                decoder_input = torch.cat((decoder_input, predicted_tokens), dim = -1)
                tgt_mask = construct_future_mask(decoder_input.shape[1])

                self.assertEqual(decoder_output.shape, (batch_size, i + 1, vocab_size))
                self.assertEqual(torch.any(decoder_output == 1), False)
                self.assertEqual(torch.all(decoder_input == bos_token_id), False)

if __name__ == "__main__":
    unittest.main()