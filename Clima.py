import requests
import openai
from translate import Translator
from datetime import datetime

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

def obter_previsao_climatica(cidade, chave_api):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={chave_api}"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados


def traduzir_texto(texto, idioma_destino):
    translator = Translator(to_lang=idioma_destino)
    traducao = translator.translate(texto)
    return traducao


def exibir_previsao(dados, idioma_destino):
    if dados["cod"] == "200":
        previsoes = dados["list"]
        print(f"Previsão do tempo para {dados['city']['name']}:")
        data_atual = None
        for previsao in previsoes:
            data_hora = previsao["dt_txt"]
            data, hora = data_hora.split(" ")
            data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Verifica se a data mudou para exibir a previsão do dia
            if data != data_atual:
                temperatura = previsao["main"]["temp"] - 273.15
                temperatura_formatada = "{:.1f}".format(temperatura)
                descricao = previsao["weather"][0]["description"]

                descricao_traduzida = traduzir_texto(descricao, idioma_destino)

                print(f"Data: {data_formatada}")
                print(f"Temperatura: {temperatura_formatada}°C")
                print(f"Descrição: {descricao_traduzida}")
                print("-" * 30)

            data_atual = data
        resposta_usuario = input("Gostaria de saber como agir diante dessa previsão? (Sim/Não): ")

        while resposta_usuario.lower() not in ["sim", "não"]:
            resposta_usuario = input("Resposta inválida. Digite 'Sim' ou 'Não': ")

        if resposta_usuario.lower() == "sim":
            pergunta_chatgpt = f"Eu sou agricultor da cidade {dados['city']['name']}. Quais devem ser as atitudes que eu devo ter segundo as seguintes previsões climáticas:\n Temperatura:{temperatura_formatada}°C,\nDescrição: {descricao_traduzida}?"
            resposta_chatgpt = obter_resposta_chatgpt(pergunta_chatgpt)
            print(f"{resposta_chatgpt}")

        print("-" * 30)
    else:
        print("Erro ao obter a previsão do tempo.")


chave_api = "8f265fcf512688921bfe4bc8d5781443"
idioma_destino = "pt"
cidade = input("Digite o nome da cidade: ")
dados_previsao = obter_previsao_climatica(cidade, chave_api)
exibir_previsao(dados_previsao, idioma_destino)
