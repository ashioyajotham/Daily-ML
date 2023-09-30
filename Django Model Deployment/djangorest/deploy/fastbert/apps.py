#from django.apps import AppConfig


#class FastbertConfig(AppConfig):
#default_auto_field = "django.db.models.BigAutoField"
#name = "fastbert"

from django.apps import AppConfig
import html
import pathlib
import os

from fast_bert.prediction import BertClassificationPredictor

class WebappConfig(AppConfig):
    name = 'fastbert'
    MODEL_PATH = Path("model") # path to dir containing model
    BERT_PRETRAINED_PATH = Path("model/saved_model/") 
    LABEL_PATH = Path("label/") # path to dir containing labels.txt files for each model
    predictor = BertClassificationPredictor(model_path = MODEL_PATH/"multilabel-emotion-fastbert-basic.bin",
                                            pretrained_path = BERT_PRETRAINED_PATH, 
                                            label_path = LABEL_PATH, multi_label=True)