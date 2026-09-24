# Narrative System Foundation

## 1. Objetivo

Definir a fundação do sistema narrativo digital do T.E.C.H. Digital.

## 2. Storylet

O Storylet é uma unidade narrativa reutilizável.

Conceitualmente, um Storylet possui:

- condições de entrada;
- contexto;
- apresentação;
- opções;
- consequências;
- recompensas;
- condições de saída.

Exemplo conceitual:

```text
STORYLET
├── Conditions
├── Entry
├── Presentation
├── Choices
├── Consequences
└── Rewards
```

## 3. Quests

Uma quest organiza uma sequência ou conjunto de objetivos narrativos.

Uma quest pode:

- iniciar Storylets;
- alterar o mundo;
- envolver NPCs;
- modificar reputação;
- produzir recompensas;
- desencadear eventos;
- terminar por caminhos diferentes.

## 4. Eventos

Eventos representam acontecimentos que alteram ou revelam o estado do jogo.

Podem ser:

- locais;
- relacionados a NPCs;
- relacionados a facções;
- mundiais;
- narrativos;
- eventos especiais.

## 5. Condições e consequências

A narrativa não deve apenas apresentar texto.

Uma escolha deve poder consultar condições do estado do jogo e produzir consequências estruturadas.

```text
Estado atual
    ↓
Condições
    ↓
Storylet disponível
    ↓
Escolha do jogador
    ↓
Consequências
    ↓
Novo estado
```

## 6. Raça e perspectiva

A raça do personagem pode influenciar:

- quais Storylets aparecem;
- quais diálogos são possíveis;
- relações;
- conflitos;
- informações disponíveis;
- eventos específicos;
- interpretação de determinados acontecimentos.

O objetivo é permitir que diferentes campanhas revelem diferentes perspectivas da história maior.

## 7. Final Absoluto

O Final Absoluto é uma camada de meta-narrativa.

Uma campanha individual pode revelar somente parte da verdade. Campanhas posteriores podem revelar novos fragmentos.

O sistema deverá registrar descobertas na Meta-Progression.

O requisito final será definido por um conjunto explícito de descobertas/eventos fundamentais, e não somente pela contagem de campanhas concluídas.

## 8. Geração narrativa

Qualquer geração dinâmica deverá permanecer dentro de conteúdo e regras autorizados.

Conceitualmente:

```text
Raça
+ Local
+ NPC
+ Facção
+ Objetivo
+ Conflito
+ Estado do mundo
        ↓
Narrative Generator
        ↓
Storylet/Event válido
```

A geração não deve criar regras incompatíveis nem alterar diretamente o estado do jogo.
