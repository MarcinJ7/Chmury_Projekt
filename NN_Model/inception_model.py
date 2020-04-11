"""
Train model with InceptionV3 weights

@author: Malwina
"""

from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras import optimizers
from tensorflow.keras.applications.inception_v3 import InceptionV3

from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

import pandas as pd

tar_size = 299

# wczytanie modelu
base_model = InceptionV3(weights = 'imagenet', include_top = False, input_shape=(tar_size, tar_size, 3))

# dorobienie warstw wyjściowych
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(1, activation=None)(x)

# ostateczny model
model = Model(inputs = base_model.input, outputs = predictions)

# zamrożenie warstw
for layer in base_model.layers:
    layer.trainable = False

model.summary()

optim = optimizers.Adam()
model.compile(optim, loss='mse', metrics=['mae'])

callbacks = [
				keras.callbacks.ModelCheckpoint(  		# zapisywanie najlepszego modelu
						filepath=path_dir + 'model_inc.h5',
						monitor='val_loss',
						save_best_only=True,
				),

				keras.callbacks.EarlyStopping(      # zatrzymywanie uczenia po braku poprawy metryki
						monitor='mae',
						patience=4,
    		),

				keras.callbacks.ReduceLROnPlateau(      # poprawianie lr po utknięciu w minimum
						monitor='val_loss',
						factor=0.1,
						patience=4,
  		   ),
]

model_json = model.to_json()
with open(path_dir + 'model_inc.json', 'w') as json_file:
    json_file.write(model_json)

# Wczytanie danych do pandas df
df = pd.read_csv(path_dir + 'train.csv', sep=',', header=0, names=['filepath', 'age'])
df_val = pd.read_csv(path_dir + 'test.csv', sep=',', header=0, names=['filepath', 'age'])

# Przetworzenie zdjęć
# dane treningowe
train_datagen = ImageDataGenerator(rescale=1./255)

# dane testowe
test_datagen = ImageDataGenerator(rescale=1./255)

# Generatory do uczenia sieci
train_generator = train_datagen.flow_from_dataframe(
												dataframe=df,
												directory='',
												x_col='filepath',
												y_col='age',
												target_size=(tar_size, tar_size),
												batch_size=128,
												class_mode='raw',
                        seed=10,	)

val_generator = test_datagen.flow_from_dataframe(
												dataframe=df_val,
												directory='',
												x_col='filepath',
												y_col='age',
												target_size=(tar_size, tar_size),
												batch_size=128,
												class_mode='raw',
                        seed=10,   )

history = model.fit_generator(train_generator,
                      steps_per_epoch = 175,
                      validation_data = val_generator,
                      validation_steps = 44,
                      epochs = 10,
                      verbose = 2,
                      callbacks = callbacks)

# Wykres
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(loss))

plt.figure()
plt.plot(epochs, loss, 'bo', label='Dane treningowe')
plt.plot(epochs, val_loss, 'b', label='Dane walidacyjne')
plt.title('Wartości funkcji straty procesu uczenia')
plt.xlabel('Epoki')
plt.ylabel('Wartość funkcji straty')
plt.legend()
plt.grid(True)

plt.show()

# Zapisanie modelu do pliku json (model) i h5 (wagi)
model_json = model.to_json()
with open(path_dir + 'model_inc.json', 'w') as json_file:
    json_file.write(model_json)

model.save_weights(path_dir + 'model_inc.h5')
print('Saved model to disk')