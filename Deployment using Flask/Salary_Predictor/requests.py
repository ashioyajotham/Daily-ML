# -*- coding: utf-8 -*-
"""requests.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vff5-0xj-pz9zaBtTWPcSRjUSCpWy-Y5
"""

import requests
url = 'http://localhost:5000/api'
r = requests.post(url,json={'exp':1.8,})
print(r.json())