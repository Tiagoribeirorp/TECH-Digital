# T.E.C.H. Digital — RPG Engine Foundation

## Objetivo

O RPG Engine é a autoridade sobre as regras mecânicas do jogo. Narrative Engine, Presentation Engine e AI Layer podem consultar seu estado, mas não podem redefinir suas regras.

## 1. Responsabilidades

- estado do personagem;
- atributos e estatísticas derivadas;
- habilidades;
- testes;
- modificadores;
- combate;
- dano e efeitos;
- progressão;
- equipamentos, poderes e magias quando aplicáveis.

## 2. Princípio de autoridade

```text
Player Input
    ↓
RPG Engine
    ↓
resultado mecânico
    ↓
Campaign / Narrative State
    ↓
Presentation
```

A IA nunca decide se um teste teve sucesso, quanto dano foi causado ou quais regras foram aplicadas.

## 3. Teste básico

O material do T.E.C.H. RPG estabelece que, em regra geral, o jogador rola um d20 e obtém sucesso quando o resultado é menor ou igual à habilidade utilizada, depois dos modificadores aplicáveis.

```text
skill_value
    ↓
apply modifiers
    ↓
effective_skill
    ↓
roll d20
    ↓
roll <= effective_skill ?
   /        \
 SIM       NÃO
  ↓          ↓
sucesso     falha
```

Fonte: Capítulo 2 — regras e testes.

## 4. Modificadores

Modificadores representam fatores externos, ambiente, estado do personagem ou dificuldade.

Eles alteram o valor efetivo da habilidade para aquele teste.

O engine deverá registrar os modificadores aplicados para permitir:

- depuração;
- replay;
- testes automatizados;
- explicação do resultado ao jogador.

## 5. Testes resistidos

Testes resistidos envolvem dois ou mais participantes.

O material-fonte descreve a comparação das margens obtidas nos testes. O engine deverá preservar essa lógica e registrar:

```text
participant
skill
roll
effective_value
margin
result
```

## 6. Dano

Dano reduz Pontos de Vida (PV). A fonte pode ser física, energética, poderes, veneno, queda ou efeitos ambientais.

O sistema digital deverá tratar dano como uma operação de estado, permitindo que sua origem e seus efeitos sejam registrados.

## 7. Estatísticas derivadas

O sistema original possui estatísticas secundárias além dos atributos principais, incluindo Vida, Fadiga, Evasão, Tempo de Reação, Velocidade por Turno e Movimento.

As fórmulas e valores exatos serão transcritos do material específico antes de serem implementados.

## 8. Combate

A arquitetura do engine deve suportar o fluxo:

```text
iniciativa
   ↓
declaração de ações
   ↓
execução
   ↓
teste
   ↓
resultado
   ↓
dano / efeito
   ↓
atualização do estado
```

O mesmo núcleo deve permitir futuras extensões para combates envolvendo naves e mechas.

## 9. Determinismo

Sempre que uma regra utilizar aleatoriedade, o RPG Engine deverá ser capaz de registrar:

- origem da rolagem;
- dado utilizado;
- modificadores;
- resultado;
- regra aplicada;
- consequência.

Isso será importante para saves, testes automatizados e reprodução de situações durante desenvolvimento.

## 10. Separação de dados

Regras e conteúdo não devem ser espalhados pelo código da Godot.

Exemplo:

```text
data/
  races/
  skills/
  talents/
  spells/
  powers/
  equipment/
  creatures/
```

O engine interpreta esses dados.

## 11. Estado mínimo

A primeira implementação jogável deverá suportar:

- personagem;
- uma raça;
- atributos;
- uma habilidade;
- Vida;
- Fadiga;
- teste d20;
- dano;
- XP;
- progressão básica;
- save/load.

## 12. Regra de implementação

Não implementar fórmulas que ainda não tenham sido validadas contra o material-fonte.

Quando uma regra estiver incompleta, ela deve ser marcada como `TBD`/“a validar”, e não preenchida por suposição.

## 13. Próxima extração

Antes do código definitivo, consolidar:

1. atributos e valores;
2. estatísticas derivadas e fórmulas;
3. habilidades e categorias;
4. progressão;
5. combate;
6. equipamentos;
7. magia;
8. poderes mutantes;
9. regras raciais.

