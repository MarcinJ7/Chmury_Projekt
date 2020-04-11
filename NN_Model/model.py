"""
Build and train the model of NN

@author: Malwina
"""

import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import model_from_json
import matplotlib.pyplot as plt
import pandas as pd

tar_size = 512
shape = (tar_size, tar_size, 3)

model = tensorflow.keras.Sequential()  # rodzaj modelu sieci

# 1. Warstwa konwolucyjna, rozmiar okna: 3x3, głębia jądra: 32
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=shape))
model.add(layers.MaxPooling2D((2, 2)))

# 2. Warstwa konwolucyjna, rozmiar okna: 3x3, głębia jądra: 64
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# 3. Warstwa konwolucyjna, rozmiar okna: 3x3, głębia jądra: 128
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(256, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

# 4. Warstwa spłaszczająca dane (z 2D na 1D)
model.add(layers.Flatten())

# 5. Warstwa odrzucająca 20% danych
model.add(layers.Dropout(0.2))

# 6. Warstwa gęsta, 256 neuronów
model.add(layers.Dense(256, activation='relu'))

# 7. Warstwa wyjściowa - 1 neuron, bez funkcji aktywacji bo wyjściem ma być wartość wyjściowa (wiek)
model.add(layers.Dense(1))

# Funkcja printująca podsumowanie modelu sieci
model.summary()

# Optymalizator - Adam (prawie zawsze daje najlepsze wyniki)
optim = optimizers.Adam()

# Kompilacja modelu, loss - funkcja straty, metrics - metryka
# Funkcja straty: mse, czyli błąd średniokwadratowy, bo wyjściem jest liczba a nie klasa
# Metryka: mae, czyli średni błąd bezwględny, tak jak wyżej
model.compile(loss='mse', optimizer=optim, metrics=['mae'])

callbacks = [
    keras.callbacks.ModelCheckpoint(  # zapisywanie najlepszego modelu
        filepath=path_dir + 'model_cnn.h5',
        monitor='val_loss',
        save_best_only=True,
    ),

    keras.callbacks.EarlyStopping(  # zatrzymywanie uczenia po braku poprawy metryki
        monitor='mae',
        patience=4,
    ),

    keras.callbacks.ReduceLROnPlateau(  # poprawianie lr po utknięciu w minimum
        monitor='val_loss',
        factor=0.1,
        patience=4,
    ),
]

# Wczytanie danych do pandas df
path_dir = r'/content/drive/My Drive/colab_files/imdb/'
df = pd.read_csv(path_dir + 'train.csv', sep=',', header=0, names=['filepath', 'age'])
df_val = pd.read_csv(path_dir + 'test.csv', sep=',', header=0, names=['filepath', 'age'])

# Przetworzenie zdjęć z augumentacją, czyli "dorabianiem" nowych zdjęc
# dane treningowe
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=10,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# dane testowe
test_datagen = ImageDataGenerator(rescale=1. / 255)

# Generatory do uczenia sieci
train_generator = train_datagen.flow_from_dataframe(
    dataframe=df,
    directory='',
    x_col='filepath',
    y_col='age',
    target_size=(tar_size, tar_size),
    batch_size=128,
    class_mode='raw', )

validation_generator = test_datagen.flow_from_dataframe(
    dataframe=df_val,
    directory='',
    x_col='filepath',
    y_col='age',
    target_size=(tar_size, tar_size),
    batch_size=128,
    class_mode='raw', )

# Wytrenowanie modelu
history = model.fit(
    train_generator,
    steps_per_epoch=20,
    epochs=30,
    validation_data=validation_generator,
    callbacks=callbacks)

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
with open(path_dir + 'model_cnn.json', 'w') as json_file:
    json_file.write(model_json)

# model.save_weights(path_dir + 'model_cnn.h5')
print('Saved model to disk')