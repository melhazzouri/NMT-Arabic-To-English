# -*- coding: utf-8 -*-
"""ArabicTranslation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B-RGly2mMWsKEpdV3q2SNXRA9ZoyNOob

# Machine Translation
1- Import Dependanices

2- import dataset for training

3- Basic EDA and visualization

4- Data Cleaning

5- Tokenization and build vocabalury

6- Pad Sequence and Vectorization

7- Train model

8- Predictions

# Import Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# basic libs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
import seaborn as sns
# %matplotlib inline

# cleaning data
import re
import os
import nltk
nltk.download("stopwords")
nltk.download('punkt')

# save vocabulary in files
import pickle

# tokenization
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Model, Sequential
from keras.layers import GRU, Input, Dense, TimeDistributed, Activation, RepeatVector, Bidirectional,LSTM, Dropout
from tensorflow.keras.layers import Embedding
from keras.optimizers import Adam
from keras.losses import sparse_categorical_crossentropy
from keras.callbacks import ModelCheckpoint

"""# Import Dataset"""

df = pd.read_csv("ara_eng.txt",delimiter="\t",names=["English","Arabic"])
df.head()

df.info()

df = df [:20000]

"""# Basic EDA and visualization"""

english_sentences = df['English']
arabic_sentences = df['Arabic']
english_words_counter = collections.Counter([word for sentence in english_sentences for word in sentence.split()])
arabic_words_counter = collections.Counter([word for sentence in arabic_sentences for word in sentence.split()])

print('{} English words.'.format(len([word for sentence in english_sentences for word in sentence.split()])))
print('{} unique English words.'.format(len(english_words_counter)))
print('10 Most common words in the English dataset:')
print('"' + '" "'.join(list(zip(*english_words_counter.most_common(10)))[0]) + '"')
print()
print('{} Arabic words.'.format(len([word for sentence in arabic_sentences for word in sentence.split()])))
print('{} unique Arabic words.'.format(len(arabic_words_counter)))
print('10 Most common words in the Arabic dataset:')
print('"' + '" "'.join(list(zip(*arabic_words_counter.most_common(10)))[0]) + '"')

word_count = df['English'].str.split().apply(len).value_counts()
word_dict = dict(word_count)
word_dict = dict(sorted(word_dict.items(), key=lambda kv: kv[1]))
index  = np.arange(len(word_dict))
values1 = word_dict.values()
plt.figure(figsize=(36,5))
plt.bar(index,values1)
plt.xlabel('Length of sentences in English')
plt.ylabel('occurances')
plt.xticks(index,word_dict.keys())
plt.show()

word_count = df['Arabic'].str.split().apply(len).value_counts()
word_dict = dict(word_count)
word_dict = dict(sorted(word_dict.items(), key=lambda kv: kv[1]))
index  = np.arange(len(word_dict))
values1 = word_dict.values()
plt.figure(figsize=(36,5))
plt.bar(index,values1)
plt.xlabel('Length of sentences in Arabic')
plt.ylabel('occurances')
plt.xticks(index,word_dict.keys())
plt.show()

"""# Data Cleaning"""

# clean english column
def clean_english(text):
  text=text.lower() # lower case

  # remove any characters not a-z and ?!,'
  text=re.sub(u"[^a-z!?',]"," ",text)

  # word tokenization
  text=nltk.word_tokenize(text)

  # join text
  text=" ".join([i.strip() for i in text])

  return text

df["English"]=df["English"].apply(lambda txt:clean_english(txt))

### We won't need to clean arabic text

"""# Tokenization"""

def tokenize(x):
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(x)
    return tokenizer.texts_to_sequences(x), tokenizer

"""# Padding"""

def pad(x, length=None):
    if length is None:
        length = max([len(sentence) for sentence in x])
    return pad_sequences(x, maxlen = 55, padding = 'post')

"""# Preprocess pipeline"""

def preprocess(x, y):
   
    preprocess_x, x_tk = tokenize(x)
    preprocess_y, y_tk = tokenize(y)

    preprocess_x = pad(preprocess_x)
    preprocess_y = pad(preprocess_y)

    # Keras's sparse_categorical_crossentropy function requires the labels to be in 3 dimensions
    preprocess_y = preprocess_y.reshape(*preprocess_y.shape, 1)

    return preprocess_x, preprocess_y, x_tk, y_tk

preproc_english_sentences, preproc_arabic_sentences, english_tokenizer, arabic_tokenizer = preprocess(english_sentences, arabic_sentences)

max_english_sequence_length = preproc_english_sentences.shape[1]
max_arabic_sequence_length = preproc_arabic_sentences.shape[1]
english_vocab_size = len(english_tokenizer.word_index)
arabic_vocab_size = len(arabic_tokenizer.word_index)

print("Max English sentence length:", max_english_sequence_length)
print("Max Arabic sentence length:", max_arabic_sequence_length)
print("English vocabulary size:", english_vocab_size)
print("Arabic vocabulary size:", arabic_vocab_size)

""" Convert the final prediction by our model into text form"""

def logits_to_text(logits, tokenizer):
    
    index_to_words = {id: word for word, id in tokenizer.word_index.items()}
    index_to_words[0] = '<PAD>'

    return ' '.join([index_to_words[prediction] for prediction in np.argmax(logits, 1)])

"""# Model"""

def model(input_shape, output_sequence_length, english_vocab_size, arabic_vocab_size):
    
    learning_rate = 0.003
    
    # Build the layers
    model = Sequential()
    model.add(Embedding(arabic_vocab_size, 256, input_length=input_shape[1], input_shape=input_shape[1:]))
    model.add(Bidirectional(GRU(256, return_sequences=True)))
    model.add(TimeDistributed(Dense(1024, activation='relu')))
    model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(english_vocab_size, activation='softmax'))) 

    # Compile model
    model.compile(loss=sparse_categorical_crossentropy,
                  optimizer=Adam(learning_rate),
                  metrics=['accuracy'])
    return model

preproc_english_sentences.shape

tmp_x = pad(preproc_arabic_sentences, preproc_arabic_sentences.shape[1])
tmp_x = tmp_x.reshape((-1, preproc_arabic_sentences.shape[-2]))

model = model(
    tmp_x.shape,
    preproc_english_sentences.shape[1],
    len(english_tokenizer.word_index)+1,
    len(arabic_tokenizer.word_index)+1)

model.summary()

model.fit(tmp_x, preproc_english_sentences, batch_size=64, epochs=10, validation_split=0.2)

model.save('model.h5')

"""# Predictions"""

def translation(i):
  print ("Arabic text:", arabic_sentences[i])
  print ("\nEnglish Translation:", english_sentences[i])
  print ("\nTranslation:", logits_to_text(model.predict(tmp_x[[i]])[0], english_tokenizer))

print(translation(680))

print(translation(220))

print(translation(114))