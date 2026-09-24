# T.E.C.H. Digital — Sistema de Capacidades

## Terminologia

No material original, **Capacidades** também são chamadas de **perícias**. O jogo as organiza em quatro grupos:

1. Capacidades de Combate
2. Capacidades Técnicas
3. Capacidades Sociais
4. Capacidades Arcanas

Cada Capacidade está associada a um atributo-base. fileciteturn19file17

## Pontos disponíveis

A quantidade de pontos disponíveis para distribuir nas Capacidades é determinada pela **Inteligência**.

A criação de personagem fornece um exemplo em que Inteligência 12 gera 12 pontos de Capacidades, acrescidos de 2 pontos concedidos pela raça humana no exemplo. fileciteturn19file0

## Tabela de pontos investidos

| Pontos gastos | Valor da Capacidade |
|---:|---:|
| 0 | Atributo -3 / -4 |
| 1 | Atributo -2 |
| 2 | Atributo -1 |
| 3 | Atributo |
| 4 | Atributo +1 |
| 5 | Atributo +2 |

O material apresenta a regra de que uma Capacidade sem treinamento pode continuar sendo usada, normalmente com penalidade. Algumas Capacidades são marcadas como **somente com treino** e exigem pelo menos 1 ponto investido. fileciteturn19file17

## Progressão do limite de uma Capacidade

O Capítulo 7 apresenta:

| Nível | Pontos máximos / habilidade |
|---:|---:|
| 1 | 3 |
| 3 | 4 |
| 5 | 5 |
| 7 | 6 |
| 9 | 7 |

Os valores intermediários não são apresentados nessa tabela.

Para o Digital, isso deve ser tratado como **limite de investimento por Capacidade**, até confirmação adicional do material.

## Capacidades de Combate

O material inclui, entre outras:

- Acrobacia (Reflexos) — somente com treino
- Cavalgar (Reflexos)
- Escalada (Força)
- Natação (Força)
- Salto (Força)
- Armas Brancas (Reflexos)
- Ativar Artefato (Inteligência) — somente com treino
- Escudo (Reflexos)
- Armas de Feixe (Reflexos)
- Combate Corpo a Corpo (Reflexos)
- Corrida (Saúde)
- Furtividade (Reflexos / Percepção)
- Tática (Inteligência) — somente com treino
- Armas de Longo Alcance (Reflexos)
- Arremesso (Reflexos)
- Artilharia Pesada (Reflexos) — somente com treino
- Combate e outras especializações de armas.

Algumas Capacidades de armas possuem subgrupos que precisam ser adquiridos separadamente, como Armas Brancas e Armas de Feixe. fileciteturn19file17

## Capacidades Técnicas

O material inclui, entre outras:

- Conhecimento (Inteligência) — somente com treino
- Computação (Inteligência)
- Línguas (Inteligência) — somente com treino
- Explosivos (Inteligência) — somente com treino
- Arrombamento (Inteligência) — somente com treino
- Eletrônica (Inteligência) — somente com treino
- Adestrar Animais (Inteligência) — somente com treino
- Armadilhas (Inteligência)
- Alquimia (Inteligência) — somente com treino
- Navegação (Inteligência) — somente com treino
- Astronavegação (Inteligência) — com requisito relacionado a Pilotagem
- Profissão (Inteligência) — somente com treino
- Robótica (Inteligência) — somente com treino
- Nanotecnologia (Inteligência) — somente com treino
- Arqueologia Espacial (Inteligência)
- Criptografia Avançada (Inteligência) — somente com treino.

## Capacidades Sociais

Entre as Capacidades descritas estão:

- Disfarce (Carisma)
- Intimidação (Carisma)
- Lábia (Carisma)
- Manha (Carisma) — somente com treino
- Punga (Reflexos) — somente com treino
- Procurar (Percepção)
- Sobrevivência (Percepção) — somente com treino
- Rastrear (Percepção)
- Diplomacia (Carisma).

## Capacidades relacionadas à magia

O material inclui Capacidades Arcanas e conhecimentos específicos relacionados ao sistema mágico, incluindo:

- Ativar Artefato
- Conhecimento das Runas.

O detalhamento completo das regras de magia será mantido em `MAGIC_SYSTEM.md`, evitando duplicação.

## Regra de testes

A regra geral do T.E.C.H. é:

1. identificar a Capacidade apropriada;
2. aplicar modificadores à Capacidade;
3. rolar d20;
4. obter sucesso quando o resultado for menor ou igual à Capacidade modificada, salvo regra específica.

Testes resistidos usam a margem obtida por cada participante. fileciteturn17file2

## Modelo de dados para o Digital

Cada Capacidade deverá futuramente ser representada por dados, com campos equivalentes a:

- id
- nome
- grupo
- atributo_base
- requer_treino
- custo_por_ponto
- especializações
- descrição
- regras
- modificadores
- pré-requisitos.

O documento não define ainda um formato de arquivo final; isso será decidido na fase de Data Design.

## Pontos a validar

- Lista completa e definitiva de Capacidades Arcanas.
- Todos os subgrupos de armas.
- Valores intermediários da progressão entre os níveis ímpares apresentados.
- Como pontos raciais adicionais interagem com o limite por Capacidade.
- Tratamento digital de Capacidades com dois atributos, como Furtividade.
