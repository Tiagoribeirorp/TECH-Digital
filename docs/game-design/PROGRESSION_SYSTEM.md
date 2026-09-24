# T.E.C.H. Digital — Sistema de Progressão

## Níveis

Personagens jogadores possuem níveis de **1 a 10**.

A progressão ocorre por Pontos de Evolução (PE), obtidos durante as aventuras. O material original descreve recompensas por combate, interpretação, boas ideias, uso inteligente de habilidades e outros feitos reconhecidos pelo Mestre. fileciteturn19file15

## Recompensa por desafio

A tabela de combate do material apresenta:

| Nível do desafio | Pontos de Evolução | Pontos de Nível |
|---:|---:|---:|
| 1 | 10 | 100 |
| 2 | 20 | 200 |
| 3 | 30 | 300 |
| 4 | 40 | 400 |
| 5 | 60 | 600 |
| 6 | 80 | 800 |
| 7 | 100 | 1000 |
| 8 | 140 | 1400 |
| 9 | 180 | 1800 |
| 10 | 240 | 2400 |

O texto explica que essa tabela de recompensa vale para combates individuais; quando há mais combatentes de um lado, a recompensa deve ser dividida entre os envolvidos. Há também uma regra de ajuste conforme a diferença de nível entre vencedor e derrotado. fileciteturn19file15

## Custos de evolução

O sistema de Pontos de Evolução apresenta os seguintes custos:

| Melhoria | Custo |
|---|---:|
| Aumentar atributo | 1 PE por ponto |
| Novo talento | 3 PE |
| Novo poder mutante/magia | 4 PE |
| Evoluir poder mutante/magia existente | 2 PE |
| Novo ponto em perícia | 1 PE |
| Ponto de Vida adicional | 1 PE |
| Ponto de Fadiga adicional | 1 PE |

Pontos não gastos podem ser acumulados para níveis futuros. Alguns talentos e poderes possuem pré-requisitos de nível ou atributos. O material também define que nenhum atributo pode ultrapassar 20 por meio desse sistema. fileciteturn19file15

## PE por nível

O mesmo capítulo apresenta uma segunda tabela:

| Nível | PE ganhos | Total acumulado |
|---:|---:|---:|
| 1 | - | - |
| 2 | 5 | 5 |
| 3 | 5 | 10 |
| 4 | 6 | 16 |
| 5 | 6 | 22 |
| 6 | 7 | 29 |
| 7 | 7 | 36 |
| 8 | 8 | 44 |
| 9 | 8 | 52 |
| 10 | 10 | 62 |

No nível 10, o personagem também ganha acesso a um **Poder Épico**, indicado com custo de 8 PE. fileciteturn19file15

## Inconsistência da fonte

Há uma inconsistência importante no Capítulo 15:

- a primeira tabela usa valores como 100, 200, 300... como **Pontos de Nível**;
- a segunda tabela apresenta PE por nível em valores muito menores, acumulando até 62.

O Digital **não deve escolher silenciosamente entre essas duas estruturas**.

Por enquanto, ambas ficam registradas como regras de origem. Antes da implementação definitiva da progressão, precisamos decidir com base na intenção do sistema original qual tabela será a autoridade para o jogo digital.

## Regras adicionais registradas

- PE não gastos podem ser acumulados.
- Talentos e poderes podem exigir nível/atributo.
- O Mestre pode conceder 1–2 PE extras por feitos heroicos ou bom roleplay.
- Nível 10 dá acesso a Poder Épico.
- Aumento de atributo por este sistema não pode ultrapassar 20.

## Impacto no Digital

O RPG Engine deverá separar:

`experience_points`

de

`level`

e de

`spendable_evolution_points`

até resolvermos a inconsistência da fonte.

Isso evita que uma decisão provisória contamine o modelo de dados.

## Próxima decisão de design

Antes do código, precisamos fechar:

1. qual tabela representa a progressão oficial;
2. se o PE de combate é XP bruto ou PE gastável;
3. como a experiência não-combate entra na mesma economia;
4. quando exatamente ocorre a subida de nível;
5. como o limite de Capacidades por nível se relaciona com os pontos gastos.
