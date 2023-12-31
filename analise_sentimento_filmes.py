# -*- coding: utf-8 -*-
"""Analise-sentimento-filmes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nVWBPP9PQN4Pb4Op838t9m2Saqe6n_ho

## Exemplo de aplicação de aprendizagem profunda em análise de sentimento
Adaptado do livro do Chollet (Cap. 3.5: [Deep Learning with Python](https://www.manning.com/books/deep-learning-with-python?a_aid=keras&a_bid=76564dff)).

O software aprende a classificar um comentário sobre um filme como positivo ou negativo.
"""

import keras
keras.__version__

# Se der erro no comando imdb.load_data tente pegar uma versão mais antiga
# do numpy (descomente a linha abaixo e reset o runtime). Quando fiz o vídeo
# explicando este código estava dando problema mas agora parece que foi
# resolvido

#!pip install numpy==1.16.2
import numpy as np
print(np.__version__)

"""## Usando o conjunto de dados IMDB


O IMDB é um conjunto de dados público com 50.000 comentários classificados entre positivos ou negativos. Os comentários são separados em 25.000 para treinamento e 25.000 para teste. É um conjunto de dados balanceado (50% de comentários positivos e 50% de negativos). Os comandos abaixo carregam o conjunto de dados IMDB.
"""

from keras.datasets import imdb

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

"""`num_words=10000` significa que apenas as 10.000 palavras mais frequentes dos comentários serão utilizadas no treinamento. Palavras mais raras serão descartadas.

As variáveis `train_data` and `test_data` são listas de comentários e cada comentário é uma lista de "índices" para palavras (cada número corresponde a uma palavra diferente)

As variáveis `train_labels` and `test_labels` são listas de 0s e 1s,  onde 0 significa um comentário "negativo" e 1 significa um comentário "positivo"

O comando abaixo mostra um único comentário e depois a sua classificação (como positivo, 1)
"""

train_data[0]

train_labels[0]

"""Os comandos abaixo mostram a primeira sentença "decodificada" (com as palavras ao invés de números)"""

# word_index é o dicionário que mapeia cada palavra em um número
word_index = imdb.get_word_index()
# Aqui nós invertemos o mapeamento pois queremos mapear os números em palavras
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
# Abaixo uma sequência é decodificada usando o dicionários. O i-3 é porque os 3 primeiros índices são reservados.
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])

decoded_review

"""uracy
## Preparação dos dados

Para usar as redes neurais profundas no Keras é preciso alterar o formato da entrada (precisa ser um tensor e não uma lista). Neste exemplo é  usado um método bem simples mas existem outras formas mais eficientes (E.g.: word embeddings). No método simples, para cada comentário, é criado um vetor (que é um tipo de tensor) com 10.000 posições em que cada posição conterá 1 ou 0 para indicar se aquela palavra está ou não presente no comentário.

"""

def vectorize_sequences(sequences, dimension=10000):
    # Cria uma matriz zerada para todos os vetores que serão associados a cada comentário
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

"""Exemplo de como um comentário é representado agora (note que se perde informação sobre a sequência e agora sabemos apenas se uma determinada palavra está ou não presente no comentário)

"""

x_train[0]

"""As listas com as classificações também precisam ser transformadas em vetores/tensores"""

y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

"""## Construindo a rede neural profunda

Vamos agora iniciar a criação de uma rede com arquitetura de 3 camadas (além da camada de entrada), todas completamente conectadas (Dense) e com a função de ativação "Relu" para as camadas ocultas e "sigmoid" para a camada de saída.
"""

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

"""Por fim, a rede é criada usando como função de perda a entropia cruzada binária (binary_crossentropy) e técnica de otimização baseada na propagação da raiz do erro quadrático médio (rmsprop) com taxa de aprendizagem (lr) de 0.001. A métrica acurácia (accuracy) é usada na validação do modelo."""

from keras import optimizers

model.compile(optimizer=optimizers.RMSprop(lr=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

"""## Aprendendo e monitorando o aprendizado usando um conjunto de validação

Um conjunto de validação contendo 10.000 dos 25.000 exemplos de treinamento é criado abaixo.
"""

x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

"""Abaixo ocorre o treinamento da rede usando 20 épocas e tamanho do lote igual a 512."""

history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(x_val, y_val))

"""A variável "history" irá conter informações úteis para analisar o treinamento"""

history_dict = history.history
history_dict.keys()

"""O código abaixo mostra informações gráficas sobre como a perda (da função de perda) e a acurácia variaram entre as épocas para o conjunto de treinamento e de validação."""

import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

# "bo" é para linha pontilhada em azul ("blue dot")
plt.plot(epochs, loss, 'bo', label='Perda no treinamento')
# "b" é para linha solida em azul
plt.plot(epochs, val_loss, 'b', label='Perda na validação')
plt.title('Perda no treinamento e na validação')
plt.xlabel('Epocas')
plt.ylabel('Perda')
plt.legend()

plt.show()

plt.clf()
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']

plt.plot(epochs, acc, 'bo', label='Acurácia no treinamento')
plt.plot(epochs, val_acc, 'b', label='Acurácia na validação')
plt.title('Acurácia no treinamento e na validação')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.legend()

plt.show()

"""## Usando a rede treinada para classificar o conjunto de teste

Quanto mais próximo de 1 o valor, maior a "confiança" de que seja um comentário positivo, quanto mais próximo de 0, maior a "confiança" em um resultado negativo.
"""

predito = model.predict(x_test)
print(predito)

# Real
print(y_test)