# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#import lib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pymongo


import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.callbacks import LearningRateScheduler

print("Print version")
print(tf.version.VERSION)

# %%
# Setup Hyper Parameter
embedding_dim = 100
max_length = 40
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"
training_size= 606
test_portion=.2


# %%
# pymongo import
client = pymongo.MongoClient("mongodb://admin:Bigdata123%23@194.233.64.254:27017")
twitterdb = client["twitter2"]
tweet_source = twitterdb["tweetbyuser"]
tweets_data = tweet_source.find({},{"text":1, "tkey":1})
tweets = pd.DataFrame(list(tweets_data))
tweets = tweets.drop(columns=['_id'])


# %%
# use copy of imdb_data insted imdb_data itself
# this ensure there is no change or modification to original imdb_data
base_data = tweets.copy()
word_len = base_data.text.str.split(' ').map(len) # recalculate so there is no error
char_len = tweets.text.map(len)


# %%
# get info regarding theese data
word_len = tweets.text.str.split(' ').map(len) 
char_len = tweets.text.map(len)
print("Total Data : {}".format(len(tweets)))
print("Average Words : {}".format(word_len.mean()))
print("Maximum Words : {}".format(word_len.max()))
print("Minimum Words : {}".format(word_len.min()))
print("Average Characters : {}".format(char_len.mean()))
print("Maximum Characters : {}".format(char_len.max()))
print("Minimum Characters  : {}".format(char_len.min()))


# %%
# shuffleing data
base_data = base_data.sample(frac=1).reset_index(drop=True)



# Vectorize all sentences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(base_data.iloc[:,0])

# basicly just get info on tokenizer
word_index = tokenizer.word_index
vocab_size=len(word_index)


# %%
# converting tkey to int
base_data["tkey"] = base_data["tkey"].replace('buzzer',1)
base_data["tkey"] = base_data["tkey"].replace('nonbuzzer',0)
base_data


# %%
# Explore Test sequences after vector
label_tokenizer = Tokenizer()
label_tokenizer.fit_on_texts(base_data.iloc[:,0])
labels = base_data.iloc[:, 1] #change all labels 2 vector


# %%
# Vectorizer Layers
vectorize_layer = TextVectorization(
    max_tokens=vocab_size,
    output_sequence_length=40,
    pad_to_max_tokens=True
)
vectorize_layer.adapt(base_data["text"].to_numpy())


# %%
#check vocab size
vocab_size
base_data


# %%
# Creating Models
# Creating Models
text_clf_nn = tf.keras.Sequential([
    vectorize_layer,
    tf.keras.layers.Embedding(vocab_size, 8, input_length=max_length), 
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(16)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(8, activation='tanh'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

opt = tf.keras.optimizers.Adam(learning_rate=0.00087, epsilon=1e-02)
text_clf_nn.compile(loss='binary_crossentropy',optimizer=opt,metrics=tf.metrics.BinaryAccuracy())
#text_clf_nn.summary()



# %%
# Another Hyperparamater
initial_learning_rate = 0.00087
epochs = 1
decay = initial_learning_rate / epochs
acc_threshold = 1


# %%
# Creating callback
class myCallback(tf.keras.callbacks.Callback): 
    def on_epoch_end(self, epoch, logs={}): 
        if(logs.get('val_binary_accuracy') > acc_threshold):   
          print(f"Reached {acc_threshold} accuracy!")   
          self.model.stop_training = True
callbacks = myCallback()

# Learning rate Scheduler
def lr_time_based_decay(epoch, lr):
    if epoch<=25:
      return lr
    else:
      return lr * 1 / (1 + decay * epoch)


# %%
history = text_clf_nn.fit(base_data["text"].to_numpy(), base_data["tkey"].to_numpy(), epochs=epochs, validation_split=0.1, verbose=1,
                    callbacks=[LearningRateScheduler(lr_time_based_decay, verbose=1), callbacks])



# %%
print(text_clf_nn.predict(["JOKOWI BANGSAT"]))


# %%
text_clf_nn.save('saved_model/rnn3.tf',save_format='tf')


# %%



