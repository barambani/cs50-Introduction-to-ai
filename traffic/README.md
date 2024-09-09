# Traffic

- [Lecture](https://cs50.harvard.edu/ai/2024/notes/5/)
- [Project](https://cs50.harvard.edu/ai/2024/projects/5/traffic/#traffic)
- [Data Set](https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb.zip)


## Experimentation

experimenting with the model the current observations emerged

- adding convolution / polling layers improves the accuracy
```
keras.layers.Input(shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
keras.layers.Conv2D(64, (3, 3), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Conv2D(64, (3, 3), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Flatten(),
keras.layers.Dense(256, activation="relu"),
keras.layers.Dropout(0.5),
keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
```
```
333/333 - 2s - 6ms/step - accuracy: 0.9657 - loss: 0.1445
```
- increasing the convolutions' filter size doesn't help accuracy, is actually detrimental (tested 5 by 5), while increasing the filters number (64) improves the accuracy
```
keras.layers.Input(shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
keras.layers.Conv2D(64, (5, 5), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Conv2D(64, (5, 5), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Flatten(),
keras.layers.Dense(256, activation="relu"),
keras.layers.Dropout(0.5),
keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
```
```
333/333 - 3s - 8ms/step - accuracy: 0.0559 - loss: 3.4978
```
- reducing the dropout (from 0.5 to 0.2) improves the accuracy at training, but reduces the accuracy at validation. Increasing it (from 0.5 to 0.6) seems reducing the accuracy at traning, but the evaluation remains good. 0.5 seems a good balance.
```
keras.layers.Input(shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
keras.layers.Conv2D(64, (3, 3), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Conv2D(64, (3, 3), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Flatten(),
keras.layers.Dense(256, activation="relu"),
keras.layers.Dropout(0.2),
keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
```
```
333/333 - 3s - 8ms/step - accuracy: 0.9575 - loss: 0.2169
```
while with 0.5 dropout 
```
333/333 - 2s - 6ms/step - accuracy: 0.9657 - loss: 0.1445
```
- increasing the hiddent state units count improves the accuracy (sweetspot seems 128), while adding more hidden layers with fewer units doesn't give the same effect
```
keras.layers.Input(shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
keras.layers.Conv2D(64, (3, 3), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Conv2D(64, (3, 3), activation="relu"),
keras.layers.MaxPooling2D(pool_size=(2, 2)),
keras.layers.Flatten(),
keras.layers.Dense(128, activation="relu"),
keras.layers.Dropout(0.5),
keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
```
```
333/333 - 2s - 5ms/step - accuracy: 0.9707 - loss: 0.1126
```