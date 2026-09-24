# T.E.C.H. Digital — Atributos Secundários

## Objetivo

Este documento registra os Atributos Secundários do T.E.C.H. com base no material original. Eles serão usados pelo RPG Engine para derivar valores de combate, sobrevivência, mobilidade e interação.

## Atributos

O Capítulo 5 define oito Atributos Secundários:

- Reação
- Pontos de Vida
- Pontos de Fadiga
- Evasão
- Tempo de Reação
- Velocidade por Turno
- Movimento
- Sentidos

### Reação

**Fórmula confirmada:**

`Reação = Carisma`

Talentos podem modificar esse valor.

### Evasão

Representa a capacidade de evitar ataques.

**Fórmula confirmada:**

`Evasão = (Reflexos + Percepção) / 4`

### Aparar

Aparar é uma técnica defensiva e não é listado pelo Capítulo 5 como um dos oito Atributos Secundários.

**Valor:**

`Aparar = perícia relevante / 2`

Sua aplicabilidade depende da arma/técnica utilizada e das regras de combate.

### Bloqueio

Também é uma técnica defensiva.

**Valor:**

`Bloqueio = perícia Escudo / 2`

### Sentidos

**Fórmula confirmada:**

`Sentidos = Percepção`

### Tempo de Reação

É usado como iniciativa.

**Fórmula confirmada:**

`Tempo de Reação = Percepção + 1d20`

O resultado é utilizado para estabelecer a ordem do combate.

### Velocidade por Turno

Determina a quantidade de ações/capacidade de ação disponível na rodada.

**Fórmula confirmada:**

`Velocidade por Turno = Reflexos / 2`

### Movimento

Cada ponto de Velocidade por Turno corresponde a 1,5 m de movimento.

`1 Velocidade por Turno = 1,5 m`

A ação Correr pode dobrar essa distância conforme as regras de combate.

### Pontos de Vida

**Fórmula confirmada:**

`PV = Saúde`

Talentos podem aumentar os PV.

Ao chegar a 0 PV, o personagem fica inconsciente. A partir daí perde 1 PV adicional por rodada sem tratamento. Se os PV atingirem valor negativo igual ao atributo Saúde, o personagem morre.

### Pontos de Fadiga

**Fórmula confirmada:**

`Fadiga = Força de Vontade`

Talentos podem aumentar a Fadiga.

Fadiga é consumida por atividades prolongadas e por poderes/magia conforme suas regras específicas.

## Regras de implementação

O RPG Engine deverá calcular estes valores a partir do estado do personagem, em vez de armazenar valores derivados como autoridade independente.

Quando houver talento, equipamento, raça ou outro efeito modificando um valor, o modificador deverá ser aplicado pelo sistema de regras correspondente.

## Pontos ainda a validar

- Arredondamento de Evasão e Velocidade por Turno quando a divisão não produzir inteiro.
- Interação completa entre defesa, armadura e Evasão.
- Recuperação de Fadiga.
- Modificadores raciais e de talentos sobre os atributos secundários.

Não inventar essas regras até que o material fonte as determine.
