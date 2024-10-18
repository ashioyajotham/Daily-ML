import unittest
from typing import List, Dict, Any
import random
from random import choices

import numpy as np
import torch
from torch import nn

from lr_scheduler import NoamOpt
from transformer import Transformer
from vocabulary import Vocabulary
from utils import construct_batches

def train(
        transformer: nn.Module,
        scheduler: Any,
        criterion: Any,
        batches: Dict[str, List[torch.Tensor]],
        masks: Dict[str, List[torch.Tensor]],
        n_epochs: int,
):
    transformer.train(True)
    num_iters = 0

    for e in range(n_epochs):
        for i, (src_batch, src_mask, tgt_batch, tgt_mask) in enumerate(
            zip(batches["src"], batches["tgt"], masks["tgt"])
        ):
            encoder_output = transformer.encoder(src_batch, src_padding_mask = src_mask) #type: ignore

            decoder_output = transformer.decoder(
                tgt_batch,
                encoder_output,
                src_padding_mask = src_mask,
                future_mask = tgt_mask,
            ) #type: ignore

            decoder_output = decoder_output[:, :-1, :]
            tgt_batch = tgt_batch[:, 1:]

            # set pad tokens in the target to -100 so they don't incur a loss
            # tgt_batch[tgt_batch == transformer.padding_idx] = -100

            batch_loss = criterion(
                decoder_output.contiguous().permute(0, 2, 1),
                tgt_batch.contiguous().long(),
            )

            batch_accuracy = (
                torch.sum(decoder_output.argmax(dim=-1) == tgt_batch)
            ) / torch.numel(tgt_batch)

            if num_iters % 100 == 0:
                print(
                    f"epoch: {e}, num_iters: {num_iters}, batch_loss: {batch_loss}, batch_accuracy: {batch_accuracy}"
                )

            batch_loss.backward()
            scheduler.step()
            scheduler.optimizer.zero_grad()
            num_iters += 1

    return batch_loss, batch_accuracy

class TestTransformerTraining(unittest.TestCase):
    seed = 0
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

    def test_copy_task(self):
        device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        if device == "cpu":
            print("Using CPU")
            return
        
        synthetic_corpus_size = 600
        batch_size = 60
        n_epochs = 200
        n_tokens_in_batch = 10

        corpus = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
        vocab = Vocabulary(corpus)
        vocab_size = len(list(vocab.token_to_index.items()))
        valid_tokens = list(vocab.token_to_index.keys())[3:]
        corpus += [
            " ".join(choices(valid_tokens, k=n_tokens_in_batch))
            for _ in range(synthetic_corpus_size)
        ]

        corpus = [{"src": s, "tgt": s} for s in corpus]
        batches, masks = construct_batches(corpus, 
                                           vocab, 
                                           batch_size = batch_size,
                                           src_lang_key = "src",
                                           tgt_lang_key = "tgt",
                                           device = device)
        
        transformer = Transformer(
            hidden_dim = 512,
            ff_dim = 2048,
            num_heads = 8,
            num_layers = 2,
            max_decoding_length = 25,
            vocab_size = vocab_size,
            padding_idx = vocab.token_to_index[vocab.PAD],
            bos_idx = vocab.token_to_index[vocab.BOS],
            dropout_p = 0.1,
            tie_output_to_embedding = True,
        ).to(device)

        optimizer = torch.optim.Adam(
            transformer.parameters(), lr=0, betas = (0.9, 0.98), eps = 1e-9
        )
        scheduler = NoamOpt(
            transformer.hidden_dim, factor = 1, warmup = 400, optimizer = optimizer
        )
        criterion = nn.CrossEntropyLoss()

        latest_batch_loss, latest_batch_accuracy = train(
            transformer, criterion, batches, masks, n_epochs = n_epochs
        )
        self.assertEqual(latest_batch_loss.item() <=0.01, True)
        self.assertEqual(latest_batch_accuracy >=0.99, True)

if __name__ == "__main__":
    unittest.main()