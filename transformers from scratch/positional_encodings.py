import math
import unittest

import torch

class SinusoidEncoding(torch.nn.module):

    def __init__(self, hidden_dim, max_len = 5000):

        super().__init__()
        pos_embed = torch.zeros(max_len, hidden_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, hidden_dim, 2).float() * (-math.log(10000.0) / hidden_dim))
        pos_embed[:,0::2] = torch.sin(position * div_term)
        pos_embed[:,1::2] = torch.cos(position * div_term)
        pos_embed = pos_embed.unsqueeze(0)

        self.register_buffer("pos_embed", pos_embed, persistent = False)

    def forward(self, x):
        x = x + self.pos_embed[:, : x.size(1)]
        return x
    
class TestSinusoidEncoding(unittest.TestCase):
    def test_create_embedding(self):
        batch = 1
        dim = 3
        len = 5
        x = torch.randn(batch, len, dim)
        pos_enc = SinusoidEncoding(dim).forward(x)
        expected = torch.Tensor(
            [ 
                [
                    [
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                    ],
                    [
                        8.4147e-01,
                        5.4030e-01,
                        9.9833e-02,
                        9.9500e-01,
                        9.9998e-03,
                        9.9995e-01,
                        1.0000e-03,
                        1.0000e00,

                    ],
                    [
                        0.9093e00,
                        -0.4161e00,
                        0.4121e00,
                        -0.9119e00,
                        -0.9589e00,
                        -0.2837e00,
                        -0.5440e00,
                        -0.8391e00,
                    ],
                    [
                        9.0930e-01,
                        -4.1615e-01,
                        1.9867e-01,
                        9.8007e-01,
                        1.9999e-02,
                        9.9998e-01,
                        2.0000e-03,
                        1.0000e00,
                    ],
                ]
            ]
        )
        torch.testing.assert_close(pos_enc, expected, rtol = 10e-5, atol = 10e-5)

    def test_create_embedding_multi_batch(self):
        batch = 2
        dim = 8
        len = 3
        x = torch.zeros(batch, len, dim)
        pos_enc = SinusoidEncoding(dim).forward(x)
        expected = torch.Tensor(
            [
                [
                    [
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                    ],
                    [
                        8.4147e-01,
                        5.4030e-01,
                        9.9833e-02,
                        9.9500e-01,
                        9.9998e-03,
                        9.9995e-01,
                        1.0000e-03,
                        1.0000e00,
                    ],
                    [
                        9.0930e-01,
                        -4.1615e-01,
                        1.9867e-01,
                        9.8007e-01,
                        1.9999e-02,
                        9.9998e-01,
                        2.0000e-03,
                        1.0000e00,
                    ],
                ],
                [
                    [
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                        0.0000e00,
                        1.0000e00,
                    ],
                    [
                        8.4147e-01,
                        5.4030e-01,
                        9.9833e-02,
                        9.9500e-01,
                        9.9998e-03,
                        9.9995e-01,
                        1.0000e-03,
                        1.0000e00,
                    ],
                    [
                        9.0930e-01,
                        -4.1615e-01,
                        1.9867e-01,
                        9.8007e-01,
                        1.9999e-02,
                        9.9998e-01,
                        2.0000e-03,
                        1.0000e00,
                    ],
                ],
            ]
        )
        torch.testing.assert_close(pos_enc, expected, rtol = 10e-5, atol = 10e-5)

if __name__ == "__main__":
    unittest.main()