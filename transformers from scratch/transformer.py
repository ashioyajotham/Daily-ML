import random
import unittest
from typing import Optional
import numpy as np
import torch
from torch import nn
from torch.nn.init import xavier_uniform_
from vocabulary import Vocabulary
from encoder import TransformerEncoder
from decoder import TransformerDecoder
from utils import construct_future_mask

class Transformer(nn.Module):
    def __init__(
            self,
            hidden_dim: int,
            ff_dim: int,
            num_heads: int,
            num_layers: int,
            max_decoding_length: int,
            vocab_size: int,
            padding_idx: int,
            bos_idx: int,
            dropout_p: float,
            tie_output_to_embedding: Optional[bool] = None,
    ):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, hidden_dim, padding_idx = padding_idx)
        self.encoder = TransformerEncoder(
            self.embed, hidden_dim, ff_dim, num_heads, num_layers, dropout_p
        )
        self.decoder = TransformerDecoder(
            self.embed, hidden_dim, ff_dim, num_heads, num_layers, vocab_size, dropout_p, tie_output_to_embedding,
        )
        self.padding_idx = padding_idx
        self.bos_idx = bos_idx
        self.max_decoding_length = max_decoding_length
        self.hidden_dim = hidden_dim
        self._reset_parameters()

    def _reset_parameters(self):
        for p in self.parameters():
            if p.dim() > 1:
                xavier_uniform_(p)


class TestTransformer(unittest.TestCase):
    def test_transformer_inference(self):
        seed = 0
        torch.manual_seed(seed)
        random.seed(seed)
        np.random.seed(seed)

        corpus = [
            "Hello, my name is Jotham and I was born with the name Jotham.",
            "#RUTOMUSTGO",
        ]
        en_vocab = Vocabulary(corpus)
        en_vocab_size = len(en_vocab.token_to_index.items())
        with torch.no_grad():
            transformer = Transformer(
                hidden_dim = 512,
                ff_dim = 2048,
                num_heads = 8,
                num_layers = 6,
                max_decoding_length = 10,
                vocab_size = en_vocab_size,
                padding_idx = en_vocab.token_to_index[en_vocab.PAD],
                bos_idx = en_vocab.token_to_index[en_vocab.BOS],
                dropout_p = 0.1,
                tie_output_to_embedding = True,
            )
            transformer.eval()

            encoder_input = torch.IntTensor(
                en_vocab.batch_encode(corpus, add_special_tokens = False)
            )
            src_padding_mask = encoder_input != transformer.padding_idx
            encoder_output = transformer.encoder.forward(
                encoder_input, src_padding_mask = src_padding_mask
            )
            self.assertEqual(torch.any(torch.isnan(encoder_output)), False)

            decoder_input = torch.IntTensor(
                [[transformer.bos_idx], [transformer.bos_idx]])
            
            tgt_mask = construct_future_mask(seq_len = 1)
            for i in range(transformer.max_decoding_length):
                decoder_output = transformer.decoder(
                    decoder_input,
                    encoder_input,
                    src_padding_mask = src_padding_mask,
                    tgt_mask = tgt_mask,
                )
                predicted_tokens = torch.argmax(
                    decoder_output[:, -1, :], dim = 1
                ).unsqueeze(1)
                
                decoder_input = torch.cat((decoder_input, predicted_tokens), dim = -1)
                tgt_mask = construct_future_mask(decoder_input.shape[1])

        self.assertEqual(decoder_input.shape, (2, transformer.max_decoding_lenth + 1))
        self.assertEqual(torch.all(decoder_input == transformer.bos_idx), False)

if __name__ == "__main__":
    unittest.main()