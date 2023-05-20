import tensorflow as tf
import numpy as np
import openai

# Carregar o modelo treinado
modelo = tf.keras.models.load_model('classificador_plantas.h5')

# Função para pré-processar uma nova imagem
def preprocessar_imagem(caminho_imagem):
    imagem = tf.keras.preprocessing.image.load_img(caminho_imagem, target_size=(224, 224))
    imagem_array = tf.keras.preprocessing.image.img_to_array(imagem)
    imagem_array = np.expand_dims(imagem_array, axis=0)
    imagem_preprocessada = tf.keras.applications.resnet50.preprocess_input(imagem_array)
    return imagem_preprocessada

# Previsão em uma nova imagem
caminho_nova_imagem = 'Imagens/Teste/teste.PNG'
imagem_preprocessada = preprocessar_imagem(caminho_nova_imagem)
previsao = modelo.predict(imagem_preprocessada)
classe = np.argmax(previsao)

# Mapear o índice da classe para o nome da doença
mapa_classes = {0: 'Ferrugem', 1: 'Míldio', 2: 'Verrugose'}
doenca_detectada = mapa_classes[classe]

# Imprimir a doença detectada
print('Doença detectada:', doenca_detectada)

resposta_usuario = input("Gostaria de saber como tratar essa doença? (Sim/Não): ")

def obter_resposta_chatgpt(pergunta):
    openai.api_key = "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"
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7
    )
    return resposta.choices[0].text.strip()

while resposta_usuario.lower() not in ["sim", "não"]:
    resposta_usuario = input("Resposta inválida. Digite 'Sim' ou 'Não': ")

if resposta_usuario.lower() == "sim":
    pergunta_chatgpt = f"Estou com a doença: {doenca_detectada} em minha plantação. Isso é ruim? O que isso pode " \
                       f"causar? O que faço para resolver?"
    resposta_chatgpt = obter_resposta_chatgpt(pergunta_chatgpt)
    print("-" * 30)
    print(f"{resposta_chatgpt}")

print("-" * 30)
