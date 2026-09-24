# T.E.C.H. Digital — Race System Foundation

## Objetivo

Registrar como as raças do T.E.C.H. RPG serão representadas no jogo digital.

Este arquivo define a estrutura técnica e o princípio de conversão. Ele não deve inventar ou alterar características das raças.

## 1. Modelo de dados

Cada raça será uma definição independente:

```text
RaceDefinition
├── id
├── name
├── lore
├── culture
├── languages
├── attribute_modifiers
├── skill_modifiers
├── advantages
├── disadvantages
├── movement_rules
└── special_rules
```

## 2. Características raciais

As características raciais devem ser aplicadas durante a criação do personagem e permanecer disponíveis ao RPG Engine durante a campanha.

Exemplos de tipos de regra que o sistema precisa suportar:

- modificadores de atributos;
- defesa natural;
- visão especial;
- modificadores de movimento;
- custos diferenciados de habilidades;
- vantagens;
- desvantagens;
- regras comportamentais ou situacionais.

Os valores concretos devem ser importados do material-fonte de cada raça.

## 3. Separação entre raça e profissão

Raça e profissão não serão acopladas por código.

Uma raça poderá fornecer características próprias sem obrigar o personagem a seguir uma única profissão.

## 4. Efeito na narrativa

Além das regras mecânicas, a raça poderá influenciar:

- diálogos;
- reconhecimento por NPCs;
- relações;
- conflitos;
- Storylets disponíveis;
- informações acessíveis;
- acontecimentos específicos.

Esses efeitos narrativos devem ser definidos por dados/condições narrativas, e não embutidos diretamente na classe de raça.

## 5. Efeito na meta-narrativa

A raça também pode determinar uma perspectiva diferente da história maior.

Isso permite que:

```text
Campanha A — Raça A
        ↓
fragmentos descobertos

Campanha B — Raça B
        ↓
novos fragmentos

Campanha C — Raça C
        ↓
novos fragmentos
        ↓
Meta-Progression
        ↓
Final Absoluto
```

A raça, portanto, é simultaneamente:

- elemento de construção do personagem;
- fonte de regras;
- identidade narrativa;
- possível perspectiva da história maior.

## 6. Pipeline de criação

```text
Escolha da raça
      ↓
Carregar RaceDefinition
      ↓
Aplicar modificadores permitidos
      ↓
Criar CharacterState
      ↓
Escolher demais elementos do personagem
      ↓
Validar personagem
      ↓
Iniciar campanha
```

## 7. Regra de segurança de dados

Uma raça não deve alterar diretamente o estado da campanha.

Ela fornece regras e características. O RPG Engine aplica as regras; o Narrative Engine consulta as características quando necessário.

## 8. Próxima etapa

Criar uma especificação individual para cada raça existente no material-fonte, mantendo:

- terminologia original;
- bônus;
- penalidades;
- vantagens;
- desvantagens;
- idiomas;
- lore;
- regras especiais.

Nenhuma característica deverá ser preenchida por suposição.
