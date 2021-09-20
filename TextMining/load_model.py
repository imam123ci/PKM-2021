import os

import tensorflow as tf
from tensorflow import keras    

model = tf.keras.models.load_model('saved_model/rnn3.tf')

print(model.summary())