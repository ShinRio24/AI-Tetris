from keras import layers
import numpy as np
from keras import ops
import keras
from keras.utils import plot_model


# load the dataset
inputs = keras.Input(shape=(12,))
dense = layers.Dense(64, activation="relu")
x = dense(inputs)
outputs = layers.Dense(2)(x)
model = keras.Model(inputs=inputs, outputs=outputs, name="mnist_model")
model.summary()



model.save("tetris.keras")

#to load model = keras.models.load_model("tetris.keras")