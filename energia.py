# Contribuição de Soluções em Energias Renováveis e Sustentáveis (SERS)
import json
import math


def numero(valor, casas=1):
    texto = f"{valor:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def reais(valor):
    return "R$ " + numero(valor, 2)


class SimuladorEnergia:
    def __init__(self, caminho):
        self.caminho = caminho
        self.p = {}
        self.referencias = []
        self.descricao = ""

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.p = {nome: item["valor"] for nome, item in dados["premissas"].items()}
            self.referencias = dados["referencias"]
            self.descricao = dados["referencia"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            print("Aviso: não foi possível carregar data/energia.json. O simulador ficou indisponível.")
            return False
        return True

    def tarifa_referencia(self):
        return self.p["tarifa_sem_impostos"] / ((1 - self.p["icms"]) * (1 - self.p["pis_cofins"]))

    def consumo_cadeira(self):
        return self.p["bateria_cadeira_kwh"] * self.p["uso_diario_bateria"] / self.p["eficiencia_recarga"] * 30

    def consumo_referencia(self):
        return self.p["consumo_casa_kwh_mes"] + self.consumo_cadeira()

    def geracao_por_kwp(self):
        return self.p["irradiacao_sp"] * 30 * self.p["desempenho_sistema"]

    def completar(self, alternativa, tarifa):
        reais_mes = alternativa["kwh_mes"] * alternativa["valor_kwh"] * tarifa
        alternativa["reais_mes"] = reais_mes
        alternativa["reais_ano"] = reais_mes * 12
        alternativa["saldo_10_anos"] = reais_mes * 120 - alternativa["custo"]
        alternativa["retorno_anos"] = alternativa["custo"] / alternativa["reais_ano"] if reais_mes > 0 else None
        alternativa["co2_kg_ano"] = alternativa["kwh_mes"] * 12 * self.p["fator_emissao"]
        return alternativa

    def piso(self, luz_do_povo):
        if luz_do_povo:
            return max(self.p["consumo_minimo_kwh"], self.p["gratuidade_luz_do_povo_kwh"])
        return self.p["consumo_minimo_kwh"]

    def alternativa_eficiencia(self, consumo, tarifa, lampadas, pessoas, luz_do_povo=False):
        p = self.p
        economia_led = lampadas * p["potencia_fluorescente_w"] / 1000 * p["horas_lampada_dia"] * 30 * p["reducao_led"]
        economia_banho = pessoas * p["minutos_a_menos_banho"] / 60 * p["potencia_chuveiro_kw"] * 30
        economia = min(economia_led + economia_banho, max(consumo - self.piso(luz_do_povo), 0))
        alternativa = {
            "nome": "Eficiência (LED + banho mais curto)",
            "custo": lampadas * p["preco_led"],
            "kwh_mes": economia,
            "kwh_led": economia_led,
            "kwh_banho": economia_banho,
            "valor_kwh": 1,
        }
        return self.completar(alternativa, tarifa)

    def alternativa_solar(self, consumo, tarifa, luz_do_povo=False):
        p = self.p
        a_compensar = max(consumo - self.piso(luz_do_povo), 0)
        modulos = math.ceil(a_compensar / self.geracao_por_kwp() / p["potencia_modulo_kwp"])
        kwp = modulos * p["potencia_modulo_kwp"]
        geracao = kwp * self.geracao_por_kwp()
        valor_credito = 1 - p["parcela_fio_b_na_tarifa"] * p["fio_b_nao_compensado_2026"]
        alternativa = {
            "nome": f"Energia solar ({numero(kwp)} kWp)",
            "kwp": kwp,
            "geracao": geracao,
            "custo": kwp * 1000 * p["preco_solar_wp"],
            "kwh_mes": min(geracao, a_compensar),
            "valor_kwh": p["simultaneidade"] + (1 - p["simultaneidade"]) * valor_credito,
        }
        return self.completar(alternativa, tarifa)

    def ler_numero(self, mensagem, minimo, maximo, padrao):
        while True:
            texto = input(mensagem).strip().replace(",", ".")
            if texto == "":
                return padrao
            try:
                valor = float(texto)
            except ValueError:
                print(f"Valor inválido. Digite um número entre {numero(minimo, 0)} e {numero(maximo, 0)}, ou Enter.")
                continue
            if minimo <= valor <= maximo:
                return valor
            print(f"Valor fora da faixa. Digite um número entre {numero(minimo, 0)} e {numero(maximo, 0)}.")

    def ler_sim_nao(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "sim"):
                return True
            if resposta in ("n", "nao", "não"):
                return False
            print("Resposta inválida. Digite s para sim ou n para não.")

    def simular(self):
        consumo_ref = self.consumo_referencia()
        tarifa_ref = self.tarifa_referencia()

        print("\n===== Simulador de energia =====")
        print("Compara duas formas de baixar a conta de luz para o mesmo consumo, em 12 meses e em 10 anos.")
        print(f"Referência: {self.descricao}.")
        print(f"Nessa casa, a recarga da cadeira motorizada gasta cerca de {numero(self.consumo_cadeira())} kWh por mês.")
        print("Pegue sua conta de luz. Aperte Enter para usar o valor de referência.")

        consumo = self.ler_numero(f"\nConsumo do mês na conta, em kWh (Enter = {numero(consumo_ref, 0)}): ", 30, 2000, consumo_ref)
        luz_do_povo = self.ler_sim_nao("A conta já tem a gratuidade da Luz do Povo (Tarifa Social)? (s/n): ")
        valor = self.ler_numero("Valor da conta em R$ (Enter = usar a tarifa de referência): ", 10, 10000, None)
        consumo_pago = consumo - self.p["gratuidade_luz_do_povo_kwh"] if luz_do_povo else consumo
        tarifa = valor / consumo_pago if valor and consumo_pago > 0 else tarifa_ref
        lampadas = int(self.ler_numero("Quantas lâmpadas fluorescentes daria para trocar por LED? (Enter = 8): ", 0, 60, 8))
        pessoas = int(self.ler_numero("Quantas pessoas tomam banho de chuveiro elétrico? (Enter = 4): ", 0, 20, 4))
        tem_telhado = self.ler_sim_nao("A casa é própria e tem telhado que pega sol, sem sombra? (s/n): ")

        eficiencia = self.alternativa_eficiencia(consumo, tarifa, lampadas, pessoas, luz_do_povo)
        solar = self.alternativa_solar(consumo, tarifa, luz_do_povo)
        self.exibir_comparacao(consumo, tarifa, eficiencia, solar)
        self.exibir_recomendacao(consumo, tarifa, eficiencia, solar, tem_telhado, luz_do_povo)
        return eficiencia, solar

    def exibir_comparacao(self, consumo, tarifa, eficiencia, solar):
        print(f"\nConsumo: {numero(consumo)} kWh/mês · tarifa usada: {reais(tarifa)}/kWh")
        linhas = [
            ("Investimento", reais(eficiencia["custo"]), reais(solar["custo"])),
            ("Economia por mês (kWh)", numero(eficiencia["kwh_mes"]), numero(solar["kwh_mes"])),
            ("Economia por mês (R$)", reais(eficiencia["reais_mes"]), reais(solar["reais_mes"])),
            ("Economia em 12 meses", reais(eficiencia["reais_ano"]), reais(solar["reais_ano"])),
            ("Retorno do investimento", self.texto_retorno(eficiencia), self.texto_retorno(solar)),
            ("Saldo em 10 anos", reais(eficiencia["saldo_10_anos"]), reais(solar["saldo_10_anos"])),
            ("CO2 evitado por ano", numero(eficiencia["co2_kg_ano"]) + " kg", numero(solar["co2_kg_ano"]) + " kg"),
        ]
        print(f"\n{'':26}{'Eficiência':>20}{solar['nome']:>24}")
        for nome, a, b in linhas:
            print(f"{nome:26}{a:>20}{b:>24}")

    def texto_retorno(self, alternativa):
        if alternativa["retorno_anos"] is None:
            return "sem economia"
        if alternativa["custo"] == 0:
            return "imediato"
        return numero(alternativa["retorno_anos"]) + " anos"

    def exibir_recomendacao(self, consumo, tarifa, eficiencia, solar, tem_telhado, luz_do_povo):
        print("\nRecomendações:")
        if luz_do_povo:
            print("1. A família já tem a Luz do Povo: os primeiros 80 kWh do mês são grátis,")
            print("   então a economia só conta sobre o consumo acima disso.")
        else:
            print("1. Confira se a família tem direito à Luz do Povo (Tarifa Social): até 80 kWh grátis por mês,")
            print("   inclusive para famílias com alguém que depende de aparelho elétrico para tratamento de saúde.")
            print("   Pergunte 'tarifa social' na opção 1 do menu.")
        print(f"2. Comece pela eficiência: custa {reais(eficiencia['custo'])} e economiza cerca de "
              f"{reais(eficiencia['reais_mes'])} por mês. O banho mais curto sozinho representa "
              f"{numero(eficiencia['kwh_banho'])} kWh/mês, sem gastar nada.")
        restante = consumo - eficiencia["kwh_mes"]
        if not tem_telhado:
            print("3. Sem casa própria com telhado ao sol, instalar energia solar em casa não é viável.")
        elif restante - self.piso(luz_do_povo) < 30:
            print("3. Depois da eficiência, o consumo pago fica perto do mínimo (ou da parte grátis):")
            print("   a energia solar quase não reduziria a conta.")
        else:
            depois = self.alternativa_solar(restante, tarifa, luz_do_povo)
            print(f"3. A energia solar se paga em cerca de {self.texto_retorno(solar)}, mas exige "
                  f"{reais(solar['custo'])} de investimento e conexão na distribuidora.")
            if depois["kwp"] < solar["kwp"]:
                print(f"   Fazendo a eficiência antes, bastaria um sistema de {numero(depois['kwp'])} kWp "
                      f"({reais(depois['custo'])}).")
        print("\nLimitações: são estimativas, não resultados garantidos. Tarifa, impostos e preços mudam;")
        print("a cobrança do Fio B sobe para 75% em 2027 e 90% em 2028; não entram bandeiras nem iluminação pública.")
        print("Premissas e fontes: data/energia.json e docs/analise_energetica.md.")
        print("Aviso: este assistente NÃO é um canal oficial.")
