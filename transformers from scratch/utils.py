import unittest
from typing import Dict, List, Tuple, Optional
import torch
from vocabulary import Vocabulary

def construct_future_mask(seq_len: int):
    subsequent_mask = torch.triu(torch.full((seq_len, seq_len), 1), diagonal=1)
    return subsequent_mask == 0

def construct_batches(
        corpus: List[Dict[str, str]],
        vocab: Vocabulary,
        batch_size: int,
        src_lang_key: str,
        tgt_lang_key: str,
        device: Optional[torch.device] = None,      
) -> Tuple[Dict[str, List[torch.Tensor]], Dict[str, List[torch.Tensor]]]:
    
    pad_token_id = vocab.token_to_index[vocab.PAD]
    batches: Dict[str, List] = {"src":[], "tgt":[]}
    masks: Dict[str, List] = {"src":[], "tgt":[]}
    for i in range(0, len(corpus), batch_size):
        src_batch = torch.IntTensor(
            vocab.batch_encode(
                [pair[src_lang_key] for pair in corpus[i: i + batch_size]],
                add_special_tokens = True,
                padding = True,
            )
        )
        tgt_batch = torch.IntTensor(
            vocab.batch_encode(
                [pair[tgt_lang_key] for pair in corpus[i: i + batch_size]],
                add_special_tokens = True,
                padding = True,
            )
        )

        src_padding_mask = src_batch != pad_token_id
        future_mask = construct_future_mask(tgt_batch.shape[-1])

        if device is not None:
            src_batch = src_batch.to(device)
            tgt_batch = src_batch.to(device)
            src_padding_mask = src_padding_mask.to(device)
            future_mask = future_mask.to(device)

        batches["src"].append(src_batch)
        batches["tgt"].append(tgt_batch)
        masks["src"].append(src_padding_mask)
        masks['tgt'].append(future_mask)

    return batches, masks

class TestUtils(unittest.TestCase):
    def test_construct_future_mask(self):
        mask = construct_future_mask(3)
        torch.testing.assert_close(
            mask,
            torch.BoolTensor(
                [[True, False, False], [True, True, False], [True, True, True]]
            ),
        )

    def construct_future_mask_first_decoding_step(self):
        mask = construct_future_mask(1)
        torch.testing.assert_close(
            mask, torch.BoolTensor([[True]]),
        )

    def test_construct_batches(self):
        corpus = [
            {"en": "This is an English sentence.", "nl": "Dit is een Nederlandse zin."},
            {"en": "The weather is nice today.", "nl": "Het is lekker weer vandaag."},
            {
                "en": "Yesterday I drove to a city called Amsterdam in my brand new car.",
                "nl": "Ik reed gisteren in mijn gloednieuwe auto naar Amsterdam.",
            },
            {
                "en": "You can pick up your laptop at noon tomorrow.",
                "nl": "Je kunt je laptop morgenmiddag komen ophalen.",
            },
            ]
        en_sentences, nl_sentences = (
            [d["en"] for d in corpus],
            [d["nl"] for d in corpus],
        )

        vocab = Vocabulary(en_sentences + nl_sentences)
        batches, masks = construct_batches(
            corpus, vocab, batch_size = 2, src_lang_key = "en", tgt_lang_key="nl"
        )
        torch.testing.assert_close(
            batches["src"],
            [
                torch.IntTensor(
                    [[0, 3, 4, 5, 6, 7, 8, 1], [0, 9, 10, 4, 11, 12, 8, 1]]
                ),
                torch.IntTensor(
                    [
                        [0, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 8, 1],
                        [0, 26, 27, 28, 29, 30, 31, 32, 33, 34, 8, 1, 2, 2, 2, 2],
                    ]
                ),
            ],
        )
