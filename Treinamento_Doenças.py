import tensorflow as tf
import os
import numpy as np

# Definindo os caminhos para os dados de treinamento
caminho_ferrugem = 'Imagens/Ferrugem'
caminho_mildio = 'Imagens/Míldio'
caminho_verrugose = 'Imagens/Verrugose'

# Criando uma lista com os caminhos das imagens de treinamento para cada classe
caminhos_ferrugem = [os.path.join(caminho_ferrugem, nome) for nome in os.listdir(caminho_ferrugem)]
caminhos_mildio = [os.path.join(caminho_mildio, nome) for nome in os.listdir(caminho_mildio)]
caminhos_verrugose = [os.path.join(caminho_verrugose, nome) for nome in os.listdir(caminho_verrugose)]
caminhos_imagens = caminhos_ferrugem + caminhos_mildio + caminhos_verrugose

# Criando rótulos para as imagens de treinamento
rotulos_ferrugem = [0] * len(caminhos_ferrugem)
rotulos_mildio = [1] * len(caminhos_mildio)
rotulos_verrugose = [2] * len(caminhos_verrugose)
rotulos = rotulos_ferrugem + rotulos_mildio + rotulos_verrugose

# Convertendo os rótulos em um array NumPy
rotulos = np.array(rotulos)

# Carregando as imagens de treinamento e redimensionando-as
imagens = []
for caminho in caminhos_imagens:
    imagem = tf.keras.preprocessing.image.load_img(caminho, target_size=(224, 224))
    imagem_array = tf.keras.preprocessing.image.img_to_array(imagem)
    imagens.append(imagem_array)
imagens = np.array(imagens)

# Pré-processamento dos dados de treinamento
imagens = tf.keras.applications.resnet50.preprocess_input(imagens)

# Carregando um modelo pré-treinado, como o ResNet50
modelo_base = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Congelando os pesos do modelo base
modelo_base.trainable = False

# Adicionando camadas adicionais para a classificação
modelo = tf.keras.models.Sequential()
modelo.add(modelo_base)
modelo.add(tf.keras.layers.GlobalAveragePooling2D())
modelo.add(tf.keras.layers.Dense(128, activation='relu'))
modelo.add(tf.keras.layers.Dense(3, activation='softmax'))

# Compilando o modelo
modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Treinando o modelo
modelo.fit(imagens, rotulos, epochs=10, batch_size=32)

# Salvando o modelo treinado
modelo.save('classificador_plantas.h5')

print("Treinamento Realizado!")
