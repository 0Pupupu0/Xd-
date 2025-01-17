# -*- coding: utf-8 -*-
"""NewLvLNeiro.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SKrRbiSyz-f4976zTFO8tbZoSUHnR3fB
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.datasets import mnist   #библиотека базы выборок

"""Загрузка обучающей и тестовой выборки"""

(x_train, y_train), (x_test, y_test) = mnist.load_data()

"""Нормализация входных данных"""

x_train = x_train/255
x_test = x_test/255

"""Преобразование выходных значений в векторы по категориям"""

y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

"""Отображение первых 25 значений из обучающей выборки"""

plt.figure(figsize=(10,5))
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.xticks([])
  plt.yticks([])
  plt.imshow(x_train[i], cmap=plt.cm.binary)

plt.show()

"""Формирование модели НС и вывод еёструктуры в консоль"""

model = keras.Sequential([
    Flatten(input_shape=(28,28,1)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
  ])

print(model.summary())

"""Компиляция НС с оптимизацией по Adam и критерием - Категориальная кросс-энтропия"""

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""Запуск процесса обучения:80%-обучающая выбоорка,20%-выборка валидации"""

model.fit(x_train, y_train_cat, batch_size=32, epochs=5, validation_split=0.2)

model.evaluate(x_test, y_test_cat)

"""Проверка распознования цифр"""

n = 0
x = np.expand_dims(x_test[n], axis=0)
res = model.predict(x)
print(res)
print(f"Распознанная цифра: {np.argmax(res)}")

plt.imshow(x_test[n], cmap=plt.cm.binary)
plt.show()

"""Распознование всей тестовоой выборки"""

pred = model.predict(x_test)
pred = np.argmax(pred, axis=1)

print(pred.shape)

print(pred[:20])
print(y_test[:20])

"""Выделение неверных вариантов"""

mask = pred == y_test
print(mask[:10])

x_false = x_test[~mask]
p_false = pred[~mask]

print(x_false.shape)

"""Вывод первых 5 неверных результатов"""

for i in range(5):
  print("Значение сети: "+str(p_false[i]))
  plt.imshow(x_false[i], cmap=plt.cm.binary)
  plt.show()