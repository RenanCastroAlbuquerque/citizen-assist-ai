import csv
import json
import os
import time
from datetime import datetime

CAMPOS_CSV = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
              "ajudou", "tentativas", "tempo_segundos", "facilidade"]
LIMITE_CARACTERES = 200


class Assistente:
    def __init__(self, nome, base, pasta_dados="data"):
        self.nome = nome
        self.base = base
        self.caminho_historico = os.path.join(pasta_dados, "historico.json")
        self.caminho_csv = os.path.join(pasta_dados, "atendimentos.csv")
        self.historico = []
        self.atendimentos_sessao = []
        self.carregar_historico()

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                self.historico = dados
            else:
                print("Aviso: o histórico estava em formato errado e foi reiniciado.")
        except FileNotFoundError:
            self.historico = []
        except json.JSONDecodeError:
            print("Aviso: o histórico estava corrompido e foi reiniciado.")
            self.historico = []

    def salvar_historico(self):
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Aviso: não foi possível salvar o histórico.")

    def ler_opcao(self, mensagem, maximo):
        while True:
            texto = input(mensagem).strip()
            if texto.isdigit() and 0 <= int(texto) <= maximo:
                return int(texto)
            print(f"Opção inválida. Digite um número de 0 a {maximo}.")

    def ler_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "sim"):
                return True
            if resposta in ("n", "nao", "não"):
                return False
            print("Resposta inválida. Digite s para sim ou n para não.")

    def tem_dado_pessoal(self, texto):
        digitos = sum(1 for letra in texto if letra.isdigit())
        return digitos >= 8 or "@" in texto

    def perguntar(self):
        print("\nEscreva sua dúvida com suas palavras.")
        print("Não informe nome, CPF, telefone ou e-mail.")
        inicio = None
        tentativas = 0
        ultima_pergunta = ""
        encontrou = False
        ultimo_id = None

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

            if pergunta == "0":
                if tentativas > 0:
                    tempo = round(time.time() - inicio, 1)
                    self.registrar("pergunta", ultima_pergunta, ultimo_id,
                                   encontrou, False, tentativas, tempo)
                return
            if pergunta == "":
                print("Você não digitou nada. Escreva sua dúvida ou 0 para voltar.")
                continue
            if self.tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva sua dúvida.")
                continue
            if len(pergunta) > LIMITE_CARACTERES:
                print(f"Sua dúvida ficou muito longa. Use no máximo {LIMITE_CARACTERES} caracteres.")
                continue

            if inicio is None:
                inicio = time.time()
            tentativas += 1
            ultima_pergunta = pergunta
            resultados = self.base.buscar(pergunta)

            if not resultados or resultados[0][0] < 3:
                print("\nNão encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras, como: BPC, passe livre, cadeira de rodas, conta de luz.")
                print("Ou volte ao menu e navegue pelas categorias: " + ", ".join(self.base.categorias()) + ".")
                continue

            pontos, melhor = resultados[0]
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            tempo = round(time.time() - inicio, 1)
            encontrou = True
            ultimo_id = melhor.id

            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir()
            alternativas = [item for item in resultados[1:3] if item[0] >= 3]
            if alternativas:
                print("\nOutras orientações que podem ajudar:")
                for pontos_alt, orientacao in alternativas:
                    print(f"  - {orientacao.titulo} ({pontos_alt} pontos)")

            ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
            if ajudou or not self.ler_sim_nao("Quer tentar com outras palavras? (s/n): "):
                self.registrar("pergunta", pergunta, melhor.id, True, ajudou, tentativas, tempo)
                inicio = None
                tentativas = 0
                ultima_pergunta = ""
                encontrou = False
                ultimo_id = None

    def navegar(self):
        categorias = self.base.categorias()
        while True:
            print("\nCategorias:")
            for numero, categoria in enumerate(categorias, start=1):
                print(f"  {numero} - {categoria}")
            print("  0 - Voltar")
            escolha = self.ler_opcao("Escolha uma categoria: ", len(categorias))
            if escolha == 0:
                return

            categoria = categorias[escolha - 1]
            orientacoes = self.base.por_categoria(categoria)
            inicio = time.time()
            while True:
                print(f"\n{categoria}:")
                for numero, orientacao in enumerate(orientacoes, start=1):
                    print(f"  {numero} - {orientacao.titulo}")
                print("  0 - Voltar")
                escolha = self.ler_opcao("Escolha uma orientação: ", len(orientacoes))
                if escolha == 0:
                    break

                orientacao = orientacoes[escolha - 1]
                tempo = round(time.time() - inicio, 1)
                orientacao.exibir()
                ajudou = self.ler_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", "Categoria: " + categoria, orientacao.id,
                               True, ajudou, 1, tempo)
                inicio = time.time()

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo):
        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "facilidade": None,
        }
        self.historico.append(atendimento)
        self.atendimentos_sessao.append(atendimento)
        self.salvar_historico()

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return None

        encontrados = [a for a in self.historico if a.get("encontrou")]
        ajudaram = [a for a in self.historico if a.get("ajudou")]
        tempos = [a.get("tempo_segundos", 0) for a in encontrados]
        tentativas = [a.get("tentativas", 1) for a in self.historico]
        notas = [a["facilidade"] for a in self.historico if a.get("facilidade")]
        sem_solucao = [a.get("pergunta", "") for a in self.historico if not a.get("ajudou")]

        resultado = {
            "total": total,
            "encontrada_pct": round(len(encontrados) / total * 100, 1),
            "ajudou_pct": round(len(ajudaram) / total * 100, 1),
            "tempo_medio": round(sum(tempos) / len(tempos), 1) if tempos else 0,
            "tentativas_media": round(sum(tentativas) / total, 1),
            "facilidade_media": round(sum(notas) / len(notas), 1) if notas else None,
            "sem_solucao": sem_solucao,
        }

        print("\n===== Indicadores =====")
        print(f"Atendimentos registrados: {resultado['total']}")
        print(f"Resposta encontrada: {resultado['encontrada_pct']}%")
        print(f"Taxa de acerto (ajudou): {resultado['ajudou_pct']}%")
        print(f"Tempo médio para encontrar: {resultado['tempo_medio']} s")
        print(f"Tentativas por atendimento: {resultado['tentativas_media']}")
        if resultado["facilidade_media"] is None:
            print("Facilidade de uso: ainda sem notas")
        else:
            print(f"Facilidade de uso: {resultado['facilidade_media']} de 5")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  nenhuma")
        return resultado

    def exportar_csv(self):
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV)
                escritor.writeheader()
                for atendimento in self.historico:
                    escritor.writerow({campo: atendimento.get(campo, "") for campo in CAMPOS_CSV})
            print(f"{len(self.historico)} atendimento(s) exportado(s) para {self.caminho_csv}")
        except OSError:
            print("Erro: não foi possível exportar o CSV.")

    def pedir_nota(self):
        if not self.atendimentos_sessao:
            return
        while True:
            texto = input("\nDe 1 a 5, o quanto foi fácil usar o assistente? ").strip()
            if texto in ("1", "2", "3", "4", "5"):
                for atendimento in self.atendimentos_sessao:
                    atendimento["facilidade"] = int(texto)
                self.salvar_historico()
                print("Obrigado pela avaliação!")
                return
            print("Nota inválida. Digite um número de 1 a 5.")
