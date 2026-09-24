# T.E.C.H. Digital — Architecture 1.0

## 1. Objetivo

Definir a arquitetura-base do T.E.C.H. Digital antes da implementação do jogo.

A arquitetura separa regras, narrativa, estado do mundo, meta-progressão e apresentação. A camada de IA é opcional e não possui autoridade sobre o estado do jogo.

## 2. Princípio de ouro

> **A IA nunca será a dona do jogo.**

O jogo deve ser completo e jogável sem depender de um modelo externo.

Quando habilitada, a IA poderá enriquecer textos, diálogos, descrições ou interpretação de intenção, mas não deverá determinar regras, resultados de testes, dano, inventário, progressão, consequências ou estado persistente.

## 3. Camadas

### RPG Engine

Responsável pelas regras do RPG:

- personagem;
- raça;
- atributos;
- estatísticas derivadas;
- habilidades;
- talentos;
- poderes;
- magias;
- equipamentos;
- inventário;
- combate;
- dano e efeitos;
- experiência;
- evolução.

### Narrative Engine

Responsável pela estrutura narrativa:

- histórias;
- quests;
- eventos;
- Storylets;
- condições;
- opções;
- consequências;
- recompensas;
- geração controlada de combinações narrativas.

### World Engine

Responsável pelo estado persistente do mundo:

- planetas;
- regiões;
- cidades;
- locais;
- NPCs;
- facções;
- relações;
- reputação;
- objetivos;
- eventos mundiais;
- alterações provocadas pelo jogador.

### Meta-Progression

Responsável pelo estado que existe acima de uma campanha individual:

- raças concluídas;
- fragmentos descobertos;
- eventos fundamentais descobertos;
- conhecimento/lore;
- finais descobertos;
- desbloqueios;
- estado necessário para o Final Absoluto.

### Presentation Engine

Responsável por transformar resultados dos sistemas em apresentação:

- cenas;
- interface;
- texto;
- diálogos;
- áudio;
- efeitos;
- transições;
- animações;
- eventos especiais.

Tipos conceituais:

- `STANDARD`
- `TRANSITION`
- `ATMOSPHERIC`
- `MAJOR_EVENT`
- `ABSOLUTE_EVENT`

A Presentation Engine não decide as regras do jogo. Ela apresenta acontecimentos já determinados pelos sistemas.

### Optional AI Layer

Camada opcional de enriquecimento.

Pode auxiliar em:

- variações de descrição;
- diálogos;
- ambientação;
- interpretação de intenção do jogador;
- geração de texto dentro de limites autorizados.

Não pode ser autoridade para:

- regras;
- estado;
- resultados de combate;
- dano;
- progressão;
- inventário;
- consequências;
- desbloqueios.

## 4. Fluxo geral

```text
                    T.E.C.H. DIGITAL
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
 RPG ENGINE        NARRATIVE ENGINE      WORLD ENGINE
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                   META-PROGRESSION
                           │
                 PRESENTATION ENGINE
                           │
                    OPTIONAL AI
                           │
                         GODOT
                           │
                         STEAM
```

A AI é uma camada opcional de enriquecimento; ela não fica no caminho obrigatório das regras.

## 5. Estado do jogo

### CharacterState

Representa o estado do personagem dentro de uma campanha.

Inclui conceitualmente:

- raça;
- nível;
- atributos;
- habilidades;
- talentos;
- poderes;
- magias;
- equipamentos;
- inventário;
- Vida;
- Fadiga;
- experiência;
- outros estados derivados necessários ao sistema.

### CampaignState

Representa uma campanha em andamento.

Inclui conceitualmente:

- CharacterState;
- quests ativas;
- quests concluídas;
- NPCStates;
- FactionStates;
- LocationStates;
- decisões;
- eventos ocorridos;
- descobertas;
- estado relevante do mundo.

### MetaProgressionState

Representa informações persistentes entre campanhas.

Inclui conceitualmente:

- raças concluídas;
- fragmentos;
- grandes eventos descobertos;
- lore;
- finais descobertos;
- desbloqueios;
- `AbsoluteEndingUnlocked`.

## 6. Final Absoluto

O Final Absoluto pertence à meta-progressão e não deve ser tratado simplesmente como:

```text
raças concluídas == todas
```

A conclusão das campanhas serve como parte do caminho. O desbloqueio deverá depender também das descobertas/eventos fundamentais definidos pelo design narrativo.

A implementação exata dos requisitos será definida na especificação narrativa.

## 7. Dados

Os sistemas devem consumir dados estruturados para conteúdo como:

- raças;
- habilidades;
- talentos;
- magias;
- poderes;
- armas;
- armaduras;
- itens;
- criaturas;
- NPCs;
- locais;
- facções;
- quests;
- Storylets;
- eventos.

A separação entre código e dados deve permitir expandir conteúdo sem reescrever o núcleo dos sistemas.

## 8. Godot

Godot será a plataforma de execução e apresentação do jogo.

Responsabilidades previstas:

- cenas;
- renderização;
- UI;
- animações;
- áudio;
- input;
- efeitos;
- gerenciamento de telas;
- execução;
- integração futura com Steam.

A lógica central deverá permanecer organizada de modo que as regras do jogo não dependam diretamente da apresentação.

## 9. Save/Load

O projeto terá dois níveis conceituais de persistência:

### Save de campanha

- personagem;
- inventário;
- quests;
- decisões;
- NPCs;
- facções;
- locais;
- eventos;
- estado do mundo.

### Perfil global

- campanhas/raças concluídas;
- fragmentos;
- descobertas;
- lore;
- finais;
- desbloqueios de meta-progressão.

## 10. Diretriz de implementação

O primeiro objetivo técnico não é construir o jogo inteiro.

É construir um pequeno ciclo jogável de ponta a ponta que prove a integração entre:

```text
Character
  ↓
Location
  ↓
NPC
  ↓
Quest
  ↓
Choice
  ↓
Combat
  ↓
Result
  ↓
XP
  ↓
Consequence
  ↓
Save
```

Esse ciclo será o primeiro alvo de implementação.
