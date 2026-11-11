# Análise energética – contribuição de SERS

Soluções em Energias Renováveis e Sustentáveis · Global Solution 2026.2 · FIAP

Integrantes: Renan de Castro Albuquerque (RM 570532), André Santos de Azevedo (RM 572236) e Guilherme Henrique de Almeida (RM 568708).

Esta é a parte de **energia** do Citizen Assist AI. O código está em `energia.py`, os dados e premissas em `data/energia.json`, e a função aparece na **opção 5 do menu** (Simulador de energia) e nas orientações da categoria **Energia** (ids 10 a 13 de `data/base_conhecimento.json`).

## 1. Público e necessidade energética

**Público:** famílias com uma pessoa com deficiência ou mobilidade reduzida, muitas de baixa renda, que dependem de aparelhos elétricos no dia a dia, como a cadeira de rodas motorizada.

**Necessidade:** reduzir o gasto com energia elétrica de uma casa que tem um consumo a mais e obrigatório: a recarga diária da cadeira motorizada. A conta pesa mais para essas famílias, e o assistente precisa dizer, com números e fontes, qual caminho faz sentido para elas.

**Casa de referência:** 4 pessoas na cidade de São Paulo, atendida pela Enel SP, ligação bifásica, com uma pessoa que usa cadeira de rodas motorizada.

## 2. Dados e premissas

Período de referência comum para as duas alternativas: **12 meses** (e o acumulado em **10 anos**, sem reajustes). Tipo: **real** = dado publicado; **estimado** = premissa do grupo, justificada.

| Dado | Valor | Tipo | Origem |
|---|---|---|---|
| Consumo médio de uma casa | 180 kWh/mês | estimado | EPE, 2025: 179,65 TWh ÷ 84,5 milhões de unidades ≈ 177 kWh/mês, arredondado |
| Bateria da cadeira motorizada | 0,912 kWh | real | Ficha técnica Dellamed D1000: 2 × 12 V × 38 Ah |
| Uso diário da bateria | 50% | estimado | Cerca de 15 km dos 30 km de autonomia do fabricante |
| Eficiência da recarga | 80% | estimado | Perdas do carregador e da bateria de chumbo-ácido |
| Tarifa Enel SP sem impostos | R$ 0,789/kWh | real | TE R$ 0,317 + TUSD R$ 0,472, vigente desde 04/07/2026 (dados ANEEL) |
| ICMS / PIS-COFINS | 12% / 9% | estimado | Mesma fonte da tarifa; variam com o consumo e o mês |
| Consumo mínimo cobrado (bifásico) | 50 kWh/mês | real | Custo de disponibilidade, REN ANEEL 1.000/2021 |
| Gratuidade Luz do Povo | 80 kWh/mês | real | MME – Luz do Povo |
| Lâmpadas fluorescentes compactas | 8 × 15 W, 4 h/dia | estimado | Casa de referência; 4 h/dia é o uso do exemplo do MME |
| Redução do LED | 35% | real | MME: LED com Selo Procel gasta até 35% menos que a fluorescente |
| Preço da lâmpada LED | R$ 12 | estimado | Conferir no comércio local |
| Chuveiro / banho mais curto | 5,5 kW / 4 min a menos por pessoa | real | Exemplo da Cemig/Agência Minas (de 12 para 8 min) |
| Irradiação solar em São Paulo | 4,589 kWh/m²·dia | real | Atlas Brasileiro de Energia Solar (INPE) |
| Desempenho do sistema solar | 75% | estimado | Perdas por temperatura, sujeira, cabos e inversor |
| Preço do sistema solar | R$ 3,00/Wp | estimado | Média residencial de R$ 2,46/Wp (Radar Solfácil, 4º tri 2024), arredondada para cima para sistemas pequenos e alta de preços em 2026 |
| Energia usada na hora (simultaneidade) | 30% | estimado | O resto vira crédito na rede |
| Peso do Fio B na tarifa | 30% | estimado | Premissa do grupo |
| Fio B não compensado em 2026 | 60% | real | Lei 14.300/2022, art. 27 (75% em 2027, 90% em 2028) |
| Fator de emissão da rede | 0,025 tCO2/MWh | real | Média dos fatores mensais do SIN de jan. a abr. de 2025 (MCTI) |

## 3. Cálculos da casa de referência

**Recarga da cadeira:** 0,912 kWh × 50% ÷ 80% × 30 dias = **17,1 kWh/mês**

**Consumo total:** 180 + 17,1 = **197,1 kWh/mês**

**Tarifa com impostos:** 0,789 ÷ [(1 − 0,12) × (1 − 0,09)] = **R$ 0,985/kWh**, o que dá uma conta de energia de cerca de **R$ 194/mês** (sem bandeiras e iluminação pública).

### Alternativa A – Eficiência (LED + banho mais curto)

- LED: 8 × 0,015 kW × 4 h × 30 dias × 35% = **5,0 kWh/mês**
- Banho: 4 pessoas × (4 ÷ 60) h × 5,5 kW × 30 dias = **44,0 kWh/mês**
- Total: **49,0 kWh/mês** → 49,0 × 0,985 = **R$ 48,32/mês**
- Investimento: 8 × R$ 12 = **R$ 96** (o banho mais curto não custa nada)

### Alternativa B – Energia solar fotovoltaica (renovável)

- Geração por kWp: 4,589 × 30 × 75% = **103,3 kWh/mês**
- Energia a compensar: 197,1 − 50 (mínimo) = **147,1 kWh/mês** → 147,1 ÷ 103,3 = 1,42 kWp → **1,5 kWp**
- Valor de cada kWh gerado: 30% usado na hora (valor cheio) + 70% em crédito, que perde 60% do Fio B (1 − 0,30 × 0,60 = 0,82) → 0,30 + 0,70 × 0,82 = **0,874 da tarifa**
- Economia: 147,1 × 0,985 × 0,874 = **R$ 126,67/mês**
- Investimento: 1.500 Wp × R$ 3,00 = **R$ 4.500**

## 4. Comparação (mesma casa, mesmo período)

| | A – Eficiência | B – Solar 1,5 kWp |
|---|---|---|
| Investimento | R$ 96 | R$ 4.500 |
| Economia por mês | 49,0 kWh · R$ 48,32 | 147,1 kWh · R$ 126,67 |
| **Economia em 12 meses** | **R$ 579,81** | **R$ 1.520,05** |
| Retorno do investimento | ~2 meses | ~3,0 anos |
| Saldo em 10 anos | R$ 5.702 | R$ 10.701 |
| CO2 evitado por ano | 14,7 kg | 44,1 kg |
| Viabilidade | Imediata, serve para quem mora de aluguel | Exige casa própria, telhado ao sol sem sombra e dinheiro ou financiamento |

### Sensibilidade: família que já tem a Luz do Povo

Com os primeiros 80 kWh grátis, a família paga só 117,1 kWh (cerca de R$ 115/mês).

| | A – Eficiência | B – Solar 1,5 kWp |
|---|---|---|
| Economia em 12 meses | R$ 579,81 | R$ 1.210,05 |
| Retorno do investimento | ~2 meses | ~3,7 anos |
| Saldo em 10 anos | R$ 5.702 | R$ 7.600 |

**Eficiência + solar juntas:** depois da eficiência, o consumo cai para 148,1 kWh/mês, e um sistema de **1,0 kWp (R$ 3.000)** já basta. Ele se paga em ~3,0 anos sem a Luz do Povo e em ~4,3 anos com ela.

## 5. Custos, viabilidade e impactos ambientais

- **Custo:** a eficiência custa R$ 96 e se paga em dois meses. A solar economiza mais no longo prazo, mas pede R$ 4.500 de uma vez, o que é difícil para uma família de baixa renda.
- **Viabilidade:** a eficiência pode ser feita por qualquer família, inclusive quem mora de aluguel. A solar depende de casa própria, telhado com sol, empresa instaladora e conexão na distribuidora. Para quem tem a Luz do Povo, o retorno da solar fica mais lento, porque os primeiros 80 kWh já são grátis.
- **Impacto ambiental:** a energia elétrica brasileira já é de baixa emissão (0,025 tCO2/MWh), então o CO2 evitado é pequeno nas duas alternativas: 14,7 kg/ano com a eficiência e 44,1 kg/ano com a solar. Os LEDs duram mais e não têm mercúrio, o que facilita o descarte (MME). A solar é uma fonte renovável e não emite durante o uso, mas a fabricação e o descarte dos painéis também têm impacto ambiental.

## 6. Recomendações e justificativas

1. **Conferir a Luz do Povo primeiro.** Ela é automática para quem está no CadÚnico e se enquadra, e inclui famílias com alguém que depende de aparelho elétrico para tratamento de saúde. É a medida de maior impacto e custo zero.
2. **Começar pela eficiência.** Ela tem o menor custo, o retorno mais rápido e serve para todas as famílias. Só o banho 4 minutos mais curto economiza 44 kWh/mês.
3. **Energia solar só depois, e se houver casa própria com telhado ao sol.** Ela traz o maior saldo em 10 anos, mas exige investimento alto. Feita depois da eficiência, o sistema pode ser menor (1,0 kWp).

## 7. Integração com o Citizen Assist AI

- **Opção 5 do menu – Simulador de energia:** a pessoa digita o consumo e o valor da sua conta de luz e responde se tem a Luz do Povo, quantas lâmpadas pode trocar, quantas pessoas tomam banho de chuveiro elétrico e se tem telhado próprio. O assistente calcula as duas alternativas e mostra a comparação, as recomendações, as limitações e onde estão as fontes. Ele não pede dados pessoais, só números de consumo.
- **Orientações da categoria Energia:** Tarifa Social / Luz do Povo (id 10), cadastro de aparelho vital (id 11), economia de energia (id 12) e energia solar (id 13). A id 13 traz o resultado desta análise e indica a opção 5.

## 8. Limitações

- Os valores são **estimativas, não resultados garantidos**. Tarifa, impostos, bandeiras e preços mudam.
- A cobrança do Fio B sobe para 75% em 2027 e 90% em 2028, o que reduz a economia da solar ao longo do tempo. A conta de 10 anos não considera isso, nem reajustes ou a troca do inversor.
- O peso do Fio B (30%), a simultaneidade (30%) e o preço por Wp são premissas do grupo. Um orçamento real pode mudar o resultado.
- A irradiação é a média anual da cidade de São Paulo. A geração varia com o mês, a inclinação e a sombra.
- O consumo da cadeira varia com o modelo e o uso.

## 9. Testes com usuários

Feito na mesma rodada do teste de Python, em 10/11/2026, com 3 pessoas de fora da equipe, sem registro de nomes ou dados pessoais. As situações de energia abaixo estão em `data/historico.json` (o simulador da opção 5 não grava histórico).

| Situação testada | Resultado | Ajuste realizado |
|---|---|---|
| Navegar pela categoria Energia e abrir "Economizar energia em casa" | Encontrou; a pessoa marcou que ajudou | Nenhum |
| Perguntar "Colocar energia solar em casa vale a pena?" | Encontrou a orientação de energia solar (id 13), com o resultado desta análise | Nenhum |
| Perguntar "Em quantos por cento seria possível economizar com energia solar, sendo que eu pago 350 em energia?" | Encontrou a orientação de energia solar, mas ela traz a estimativa da casa de referência, não a da conta da pessoa | A resposta da orientação 13 passou a explicar como estimar a economia com a própria conta na opção 5 (consumo em kWh e valor da conta) |

**Comentários recebidos:** os participantes acharam o sistema fácil e intuitivo; um deles destacou as fontes, que mostram que as informações são verídicas.

## 10. Referências

1. EPE – Anuário Estatístico de Energia Elétrica (destaques): https://dashboard.epe.gov.br/apps/anuario-livro/livro/pt/destaques.html
2. Ficha técnica da cadeira Dellamed D1000: https://www.drogasil.com.br/cadeira-de-rodas-motorizada-em-aluminio-dobravel-ate-120-kg-assento-de-45-cm-d1000-dellamed-prata-1451238.html
3. Tarifa Enel SP 2026 (dados ANEEL): https://calculadoraenergia.com.br/tarifa/enel-sp
4. Reajuste Enel SP aprovado pela ANEEL em 30/06/2026: https://www.cnnbrasil.com.br/infra/aneel-aprova-alta-de-1018-na-conta-da-enel-sp-para-89-milhoes-de-imoveis/
5. MME – Selo Procel chega às lâmpadas LED: https://www.gov.br/mme/pt-br/assuntos/noticias/selo-procel-chega-as-lampadas-led
6. Agência Minas / Cemig – pequenas mudanças na conta de luz: https://agenciaminas.mg.gov.br/noticia/confira-como-pequenas-mudancas-podem-reduzir-o-valor-da-conta-de-luz
7. Irradiação solar dos municípios paulistas (Atlas Brasileiro de Energia Solar, INPE): https://www.absolar.org.br/wp-content/uploads/2021/02/São Paulo.pdf
8. Radar Solfácil – preço da energia solar no 4º tri de 2024: https://canalsolar.com.br/energia-solar-preco-quarto-trimestre/
9. Lei 14.300/2022: https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm
10. Fatores de emissão do SIN 2025 (MCTI): https://cenarioenergia.com.br/2025/06/13/brasil-reduz-intensidade-de-carbono-na-geracao-eletrica-com-inclusao-de-novas-renovaveis-na-base-de-calculo-oficial/
11. MME – Luz do Povo: https://www.gov.br/mme/pt-br/luzdopovo
