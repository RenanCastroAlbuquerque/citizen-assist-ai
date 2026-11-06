import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

CAMPOS = ["id", "categoria", "titulo", "palavras_chave", "resposta",
          "documentos", "onde", "fonte", "verificado_em"]


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
            return False
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido (JSON inválido).")
            return False

        if not isinstance(dados, list):
            print("Erro: a base de conhecimento precisa ser uma lista de orientações.")
            return False

        self.orientacoes = []
        for registro in dados:
            if isinstance(registro, dict) and all(campo in registro for campo in CAMPOS):
                self.orientacoes.append(Orientacao(registro))
            else:
                print("Aviso: uma orientação com campos faltando foi ignorada.")
        return len(self.orientacoes) > 0

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)
        pontos = 0
        for chave in orientacao.palavras_chave:
            if normalizar(chave) in pergunta:
                pontos += 3
        for palavra in pergunta.split():
            if len(palavra) >= 4 and " " + palavra + " " in titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
