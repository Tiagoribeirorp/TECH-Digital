# Technical Overview

## Stack inicial

- **Engine:** Godot
- **Linguagem:** GDScript
- **Versionamento:** Git + GitHub
- **Distribuição planejada:** Steam

## Princípios técnicos

### Separação de responsabilidades

Regras e estado do jogo não devem depender diretamente da apresentação visual.

### Dados separados do código

Conteúdo como raças, itens, habilidades, NPCs, quests e Storylets deverá ser representado como dados estruturados sempre que isso simplificar expansão e manutenção.

### Determinismo

Resultados de regras importantes devem ser produzidos pelo sistema do jogo, permitindo reprodução, depuração e testes.

### Testabilidade

Os sistemas centrais devem poder ser testados sem exigir que toda a interface esteja carregada.

## Estrutura planejada

```text
TECH-Digital/
├── README.md
├── ARCHITECTURE.md
├── .gitignore
├── docs/
│   ├── game-design/
│   ├── narrative/
│   └── technical/
├── game/
├── data/
├── stories/
├── presentation/
├── tools/
└── tests/
```

## Primeiro alvo técnico

O primeiro protótipo deverá provar:

1. criação de personagem;
2. entrada em uma localização;
3. interação com NPC;
4. início de uma quest;
5. escolha narrativa;
6. combate;
7. aplicação de dano/efeito;
8. ganho de XP;
9. consequência narrativa;
10. Save/Load.

## Fora do escopo inicial

Neste estágio não são necessários:

- sistema completo de Steam;
- IA obrigatória;
- produção cinematográfica;
- todas as raças;
- todos os equipamentos;
- mundo completo;
- conteúdo final.

O objetivo inicial é construir uma base pequena, funcional e extensível.
