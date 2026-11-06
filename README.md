# Citizen Assist AI

Assistente de terminal, em Python, que orienta **pessoas com deficiência, pessoas com mobilidade reduzida e seus cuidadores** sobre benefícios, transporte, saúde e energia, sempre com fonte oficial e sem pedir dados pessoais.

Global Solution 2026.2 · Pensamento Computacional e Automação com Python · FIAP

## Integrantes

| Nome | RM |
|---|---|
| Renan de Castro Albuquerque | 570532 |
| André Santos de Azevedo | 572236 |
| Guilherme Henrique de Almeida | 568708 |

## Público e problema

Pessoas com deficiência e suas famílias têm direito a vários benefícios (BPC, Passe Livre, isenção de IPI, cartão de estacionamento, cadeira de rodas pelo SUS, Tarifa Social de Energia), mas a informação está espalhada em sites diferentes, com linguagem técnica. Muitas vezes quem procura é um cuidador com pouco tempo.

O Citizen Assist AI reúne essas orientações em um só lugar, em linguagem simples, mostrando os documentos necessários, onde ir, a fonte oficial e a data em que a informação foi conferida.

## ODS relacionados

- **ODS 10 – Redução das desigualdades:** facilita o acesso de pessoas com deficiência aos seus direitos.
- **ODS 3 – Saúde e bem-estar:** orienta sobre cadeira de rodas, órteses, próteses e reabilitação pelo SUS.
- **ODS 11 – Cidades e comunidades sustentáveis:** transporte e estacionamento acessíveis.
- **ODS 7 – Energia limpa e acessível:** Tarifa Social, cadastro de equipamento vital e economia de energia.

## Como executar

Requisitos: Python 3.10 ou superior. Não usa bibliotecas externas.

```bash
python main.py
```

Menu:

```
1 - Fazer uma pergunta
2 - Navegar por categorias
3 - Ver indicadores
4 - Exportar atendimentos (CSV)
0 - Sair
```

Ao sair, o assistente pede uma nota de facilidade de 1 a 5 e exporta `data/atendimentos.csv`.

## Estrutura

```
citizen-assist-ai/
├── README.md
├── main.py                  # menu principal
├── orientacao.py            # classe Orientacao
├── base_conhecimento.py     # classe BaseConhecimento + normalizar()
├── assistente.py            # classe Assistente
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

As classes se encaixam por composição:

```
Assistente
└── base: BaseConhecimento
    └── orientacoes: [Orientacao, Orientacao, ...]
```

## Base de conhecimento

`data/base_conhecimento.json` tem **12 orientações** em **4 categorias** (Benefícios e direitos, Transporte e mobilidade, Saúde e reabilitação, Energia), cada uma com pelo menos 3 palavras-chave, fonte oficial e data de verificação. O assistente só responde com o que está na base.

## Regra de pontuação

A pergunta, as palavras-chave e o título são comparados sem acentos, sem pontuação e em minúsculas (`normalizar()`).

| Regra | Pontos |
|---|---|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |

| Melhor resultado | O que acontece |
|---|---|
| 6 pontos ou mais | Confiança ALTA |
| 3 a 5 pontos | Confiança MÉDIA |
| Menos de 3 pontos | "Não encontrei": sugere outras palavras e as categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)` da maior para a menor pontuação. O assistente mostra a melhor orientação e até duas alternativas que também tenham 3 pontos ou mais.

Exemplo: "Como conseguir cadeira de rodas pelo SUS?" → +3 (`cadeira de rodas`) +3 (`cadeira de rodas pelo sus`) +1 (`conseguir` no título) +1 (`cadeira`) +1 (`rodas`) +1 (`pelo`) = **10 pontos, confiança ALTA**.

## Regras de atendimento

- Navegação por categorias numeradas, com "0 para voltar" em todas as telas.
- Opção fora da faixa, letras, resposta vazia, texto muito longo (mais de 200 caracteres) ou s/n inválido nunca encerram o programa.
- O assistente nunca pede nome, CPF, telefone ou e-mail. Pergunta com 8 ou mais dígitos ou com "@" é recusada e **não é registrada**.
- Toda resposta mostra fonte, data de verificação e o aviso de que o assistente não é canal oficial.
- Se a base estiver ausente ou corrompida, o programa avisa e encerra sem erro. Se o histórico estiver corrompido, ele é reiniciado com um aviso.

## Histórico e indicadores

Cada atendimento é salvo em `data/historico.json` com: data, origem (pergunta ou categoria), pergunta, id da orientação, se encontrou, se ajudou, tentativas, tempo em segundos e a nota de facilidade dada ao sair.

Indicadores (opção 3): resposta encontrada (%), taxa de acerto (ajudou %), tempo médio para encontrar, tentativas por atendimento, facilidade de uso (1 a 5) e lista de dúvidas sem solução. A opção 4 exporta tudo para `data/atendimentos.csv` com `csv.DictWriter`.

## Integrações com outras disciplinas

- **Computer Organization and Architecture:** o grupo desenvolveu o **Língua Livre**, um protótipo com Raspberry Pi Pico que permite a pessoas com tetraplegia controlar aparelhos com a língua. O Citizen Assist AI atende o mesmo público, com orientações sobre os direitos dessas pessoas. A integração é de tema; os códigos são independentes.
- **Soluções em Energias Renováveis e Sustentáveis:** a categoria **Energia** é o ponto de integração com a análise energética da disciplina.

## Fontes consultadas

Todas conferidas em 06/11/2026:

1. BPC à pessoa com deficiência – gov.br: https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-a-pessoa-com-deficiencia
2. Cadastro Único – gov.br: https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal
3. Isenção de IPI/IOF – Receita Federal: https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/perguntas-frequentes/isencao-para-compra-de-carro/isencao-para-compra-de-carro
4. Passe Livre interestadual – ANTT: https://www.gov.br/antt/pt-br/assuntos/passageiros/passageiros-rodoviarios/passe-livre
5. Cartão DeFis – Prefeitura de São Paulo: https://prefeitura.sp.gov.br/web/mobilidade/w/autorizacoes_especiais/cartao_de_estacionamento_defis/3557
6. Credencial de estacionamento digital – gov.br: https://www.gov.br/pt-br/servicos/emitir-credencial-de-estacionamento-digital
7. Bilhete Único Especial – SPTrans: https://bilheteunico.sptrans.com.br/especial/pessoa-com-deficiencia/
8. Cadeira de rodas pelo SUS – Ministério da Saúde: https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/e/ela/faq/faq/o-sus-oferece-cadeira-de
9. CER e Oficina Ortopédica – Ministério da Saúde: https://www.gov.br/saude/pt-br/assuntos/noticias/2022/agosto/centro-especializado-em-reabilitacao-e-oficina-ortopedica-sao-pontos-de-atencao-a-pessoa-com-deficiencia-no-sus
10. Luz do Povo / Tarifa Social – Ministério de Minas e Energia: https://www.gov.br/mme/pt-br/luzdopovo
11. Cadastro de equipamento vital – Governo do Paraná: https://www.parana.pr.gov.br/servicos/Servicos/Habitacao/Cadastrar-usuario-de-equipamento-vital-na-Copel-ZVNk7pNe
12. Economia de energia – Agência Minas (Governo de MG): https://agenciaminas.mg.gov.br/noticia/confira-como-pequenas-mudancas-podem-reduzir-o-valor-da-conta-de-luz

## Resultado do teste com usuários

> **Preencher depois do teste.** Mínimo de 3 pessoas de fora da equipe e 10 atendimentos no total. Não registrar nomes nem dados dessas pessoas.

| Participante | Atendimentos |
|---|---|
| Pessoa 1 | |
| Pessoa 2 | |
| Pessoa 3 | |
| **Total** | |

Indicadores obtidos (copiar da opção 3 do menu):

| Indicador | Resultado |
|---|---|
| Resposta encontrada | |
| Taxa de acerto (ajudou) | |
| Tempo médio para encontrar | |
| Tentativas por atendimento | |
| Facilidade de uso (1 a 5) | |

Dúvidas sem solução:

- 

Melhoria feita a partir do teste:

- 

## Limitações

- A base tem 12 orientações. Dúvidas fora delas recebem "não encontrei".
- A busca compara palavras: não entende sinônimos nem erros de digitação que não estejam nas palavras-chave.
- Regras e valores mudam. O Passe Livre, por exemplo, teve regras atualizadas em 2026; por isso cada resposta mostra a data de verificação e o aviso para confirmar no órgão oficial.
- Algumas orientações valem só para algumas cidades ou estados (Cartão DeFis e Bilhete Único Especial em São Paulo; o exemplo de cadastro de equipamento vital é da Copel, no Paraná).
- O assistente não consulta sistemas oficiais nem faz pedidos: ele só orienta.
- A média de facilidade usa a nota dada ao sair, aplicada a todos os atendimentos daquela sessão.

## Vídeo técnico

Link (YouTube, não listado): 
