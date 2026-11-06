import os

from assistente import Assistente
from base_conhecimento import BaseConhecimento

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(PASTA, "data")


def mostrar_menu():
    print("\n===== MENU =====")
    print("1 - Fazer uma pergunta")
    print("2 - Navegar por categorias")
    print("3 - Ver indicadores")
    print("4 - Exportar atendimentos (CSV)")
    print("0 - Sair")


def main():
    base = BaseConhecimento(os.path.join(PASTA_DADOS, "base_conhecimento.json"))
    if not base.carregar():
        print("O assistente não pode funcionar sem a base de conhecimento.")
        print("Verifique o arquivo data/base_conhecimento.json e tente de novo.")
        return

    assistente = Assistente("Citizen Assist AI", base, PASTA_DADOS)
    print(f"\n=== {assistente.nome} ===")
    print("Orientações para pessoas com deficiência, pessoas com mobilidade reduzida e cuidadores.")
    print("Este assistente NÃO é um canal oficial e não pede seus dados pessoais.")

    while True:
        mostrar_menu()
        opcao = assistente.ler_opcao("Escolha uma opção: ", 4)
        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.pedir_nota()
            assistente.exportar_csv()
            print("Até logo!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
