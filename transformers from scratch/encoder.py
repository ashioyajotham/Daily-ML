import math
import unittest
from typing import List, Optional

import torch
from torch import nn
from torch.nn.init import xavier_uniform_

from vocabulary import Vocabulary
from multi_head_attention import MultiheadAttention
from positional_encoding import PositionalEncoding

# We are creating an Encoder class that will be used to encode the input sequence.