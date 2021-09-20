import tensorflow as tf

model = tf.keras.models.load_model("saved_model/rnn3.tf")
rslt = model.predict(["mantap"])

print(rslt)