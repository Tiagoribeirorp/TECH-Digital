# Game Design Foundation

## Objetivo

Este documento estabelece a fundação de design do T.E.C.H. Digital.

O projeto deve preservar a identidade do T.E.C.H. RPG original enquanto adapta sua estrutura para uma experiência digital narrativa.

## Pilares

1. **RPG** — regras, atributos, habilidades, combate e progressão.
2. **Narrativa** — escolhas com consequências e múltiplos caminhos.
3. **Mundo persistente** — personagens, facções, locais e eventos podem mudar.
4. **Perspectivas múltiplas** — diferentes raças podem revelar diferentes partes da história.
5. **Meta-progressão** — descobertas de uma campanha podem ter significado em campanhas posteriores.
6. **Apresentação controlada** — a produção visual deve concentrar recursos nos acontecimentos importantes.

## Ciclo de jogo

O ciclo-base esperado é:

```text
Explorar
  ↓
Interagir
  ↓
Escolher
  ↓
Resolver
  ↓
Sofrer/produzir consequências
  ↓
Evoluir
  ↓
Descobrir
  ↓
Continuar
```

## Personagem

O personagem digital deverá representar os elementos definidos pelo RPG original, incluindo raça, atributos, habilidades e demais componentes pertinentes ao sistema.

A escolha de raça não deve, por princípio, bloquear a adaptação do personagem a uma profissão.

A implementação detalhada será especificada em documentos próprios.

## Combate

O combate digital deverá representar as regras do RPG original em uma sequência determinística e auditável pelo sistema:

```text
Iniciativa
→ Declaração
→ Execução
→ Teste
→ Resultado
→ Dano/Efeito
→ Atualização do estado
```

## Narrativa

Decisões narrativas devem produzir efeitos verificáveis no estado do jogo.

Exemplos conceituais:

- alterar relação com NPC;
- alterar reputação;
- concluir ou bloquear uma quest;
- modificar estado de uma localização;
- iniciar evento;
- produzir recompensa;
- registrar descoberta.

## Progressão

A progressão deverá utilizar o sistema de evolução definido pelo T.E.C.H. RPG, adaptando sua execução para uma interface digital.

Detalhes numéricos e regras específicas devem ser extraídos dos documentos-fonte antes de serem implementados.

## Apresentação

A maior parte da experiência pode utilizar:

- cenários estáticos;
- personagens;
- texto;
- escolhas;
- interface;
- áudio;
- efeitos simples.

Grandes acontecimentos poderão receber apresentações especiais.

## MVP

O primeiro MVP deverá ser pequeno e completo:

- uma raça;
- um personagem;
- um local;
- um NPC;
- uma missão;
- um inimigo;
- um combate;
- Vida;
- Fadiga;
- um teste de habilidade;
- XP;
- uma decisão;
- uma consequência;
- Save/Load;
- uma transição visual.

O objetivo é validar o ciclo, não quantidade de conteúdo.
