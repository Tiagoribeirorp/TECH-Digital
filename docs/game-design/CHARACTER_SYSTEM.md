# T.E.C.H. Digital — Character System Foundation

> Documento de especificação inicial. O objetivo é transportar o conceito de personagem do T.E.C.H. RPG para uma arquitetura digital sem substituir as regras originais por regras inventadas.

## 1. Personagem

No T.E.C.H. RPG, o Personagem Jogador (PJ) é o avatar do jogador no mundo e possui características, habilidades, motivações e histórico. A ficha reúne as informações importantes para sua interpretação e para a resolução das ações.

No digital, esse conceito será representado pelo `CharacterState`.

## 2. Estrutura conceitual

```text
CharacterState
├── identity
│   ├── id
│   ├── name
│   └── race
│
├── attributes
│   ├── strength
│   ├── reflexes
│   ├── health
│   ├── perception
│   ├── intelligence
│   ├── willpower
│   └── charisma
│
├── derived_stats
├── skills
├── talents
├── powers
├── spells
├── equipment
├── inventory
├── progression
└── current_state
    ├── life
    └── fatigue
```

Os nomes internos acima são identificadores conceituais; os valores, fórmulas e limites devem ser definidos a partir das regras correspondentes do T.E.C.H. RPG antes da implementação definitiva.

## 3. Atributos

A arquitetura digital prevê os sete atributos:

1. Força
2. Reflexos
3. Saúde
4. Percepção
5. Inteligência
6. Força de Vontade
7. Carisma

Este documento não fixa ainda fórmulas derivadas ou valores iniciais. Essas regras deverão ser transcritas da documentação específica do sistema.

## 4. Habilidades

O personagem utiliza habilidades/perícias para resolver ações.

A regra geral documentada no T.E.C.H. RPG é:

```text
valor da habilidade
        ↓
modificador da situação
        ↓
habilidade efetiva
        ↓
rolagem de d20
        ↓
resultado <= habilidade efetiva
        ↓
sucesso
```

Um resultado maior que a habilidade efetiva representa falha, salvo quando a descrição da ação indicar outra regra.

## 5. Testes resistidos

Testes resistidos comparam as margens obtidas pelos participantes.

Conceitualmente:

```text
Teste A → margem A
Teste B → margem B
        ↓
comparação das margens
        ↓
resultado do confronto
```

A implementação deverá preservar a regra de margem descrita no T.E.C.H. RPG.

## 6. Modificadores

Modificadores representam condições externas, ambiente, estado do personagem ou dificuldade da tarefa.

Eles são aplicados ao valor da habilidade antes da comparação com o d20.

Exemplo documentado:

```text
Pilotagem = 12
Modificador = -2
Habilidade efetiva = 10
Rolagem d20 = 8
Resultado = sucesso
```

## 7. Raça

A raça é um componente estrutural do personagem.

No jogo digital, a raça deverá ser representada por dados, e não por código específico espalhado pelo projeto.

Estrutura conceitual:

```text
RaceDefinition
├── id
├── name
├── description
├── lore
├── languages
├── attribute_modifiers
├── advantages
├── disadvantages
├── movement
└── special_rules
```

A definição exata de cada raça será transcrita a partir do material-fonte correspondente.

## 8. Raça e profissão

A arquitetura deverá permitir que a escolha de raça e a construção profissional do personagem sejam tratadas como sistemas distintos.

Isso permite preservar a possibilidade, estabelecida no material do RPG, de diferentes raças se adaptarem a diferentes profissões.

## 9. Estado derivado

Vida, Fadiga e demais estatísticas derivadas devem ser calculadas pelo RPG Engine a partir das regras oficiais.

Não devemos colocar fórmulas provisórias no código antes de validar a fonte correspondente.

## 10. Regra de implementação

O personagem não deve ser uma cena da Godot.

O ideal é:

```text
CharacterState
      ↓
RPG Engine
      ↓
Presentation/UI
```

Isso permite testar regras do personagem sem depender da interface gráfica.

## 11. Próxima etapa

Extrair, validar e registrar separadamente:

- valores iniciais;
- limites;
- custos;
- fórmulas derivadas;
- progressão;
- habilidades por categoria;
- regras específicas de cada raça.

Somente depois dessa etapa esses valores devem virar dados definitivos do jogo.
