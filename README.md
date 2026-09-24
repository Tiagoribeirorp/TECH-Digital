# T.E.C.H. Digital

> Um RPG narrativo digital baseado no universo e nas regras do T.E.C.H. RPG.

## Visão

T.E.C.H. Digital é a adaptação digital do T.E.C.H. RPG para uma experiência narrativa interativa.

O projeto combina:

- regras próprias de RPG;
- progressão de personagem;
- múltiplas raças e perspectivas;
- mundo persistente;
- decisões narrativas com consequências;
- Storylets e eventos narrativos;
- combate;
- exploração;
- múltiplos caminhos;
- meta-progressão entre campanhas;
- um Final Absoluto desbloqueado por descobertas realizadas ao longo de diferentes campanhas.

A proposta é que o jogador não apenas acompanhe uma história: suas escolhas alteram personagens, relações, missões e o estado do mundo.

## Princípio central

**A IA nunca será a dona do jogo.**

O jogo deve funcionar integralmente sem depender de um modelo externo de inteligência artificial.

A IA, quando habilitada, será uma camada opcional destinada a enriquecer a experiência — por exemplo, descrições, diálogos e variações narrativas — enquanto as regras, estados, consequências e decisões do jogo permanecem sob controle dos sistemas próprios do projeto.

## Arquitetura

A arquitetura inicial do projeto é organizada em seis sistemas principais:

1. **RPG Engine** — personagens, atributos, habilidades, combate, progressão e regras.
2. **Narrative Engine** — histórias, quests, eventos e Storylets.
3. **World Engine** — locais, NPCs, facções e estado persistente do mundo.
4. **Meta-Progression** — descobertas, campanhas concluídas, fragmentos e desbloqueios globais.
5. **Presentation Engine** — apresentação visual, transições, eventos e cenas especiais.
6. **Optional AI Layer** — camada opcional de enriquecimento narrativo.

Os dados do jogo são tratados como uma camada transversal.

### Visão geral

```text
T.E.C.H. DIGITAL
├── RPG ENGINE
├── NARRATIVE ENGINE
├── WORLD ENGINE
├── META-PROGRESSION
├── PRESENTATION ENGINE
└── OPTIONAL AI LAYER
        ↓
      GODOT
        ↓
      STEAM
```

## Conceito narrativo

Uma das ideias centrais é que diferentes raças possam revelar diferentes perspectivas de uma mesma história maior.

Uma campanha pode revelar apenas parte da verdade. Outras campanhas podem apresentar novos acontecimentos, relações, conflitos e fragmentos de conhecimento.

O **Final Absoluto** representa uma camada narrativa superior e não deve depender apenas da quantidade de campanhas concluídas: ele deverá ser associado às descobertas e eventos fundamentais necessários para compreender a história maior.

## Apresentação

A experiência não pretende depender de produção cinematográfica constante.

A maior parte das aventuras poderá utilizar cenários estáticos, personagens, texto, escolhas, interface, áudio e efeitos simples.

Transições e mudanças de contexto poderão utilizar desfoque, fade e outros efeitos atmosféricos.

Grandes acontecimentos terão apresentações especiais.

Tipos conceituais:

- `STANDARD`
- `TRANSITION`
- `ATMOSPHERIC`
- `MAJOR_EVENT`
- `ABSOLUTE_EVENT`

## Tecnologia

A plataforma inicial escolhida para o desenvolvimento é **Godot**, utilizando **GDScript**.

O objetivo é manter a arquitetura do jogo independente da engine sempre que possível, utilizando Godot principalmente para:

- renderização;
- cenas;
- interface;
- animações;
- áudio;
- entrada do jogador;
- efeitos;
- execução do jogo;
- integração futura com Steam.

## MVP

O primeiro protótipo jogável deverá ser pequeno, mas completo.

Escopo inicial:

- 1 raça;
- 1 personagem;
- 1 local;
- 1 NPC;
- 1 pequena missão;
- 1 inimigo;
- 1 combate;
- Vida;
- Fadiga;
- 1 teste de habilidade;
- XP;
- 1 decisão narrativa;
- 1 consequência;
- Save/Load;
- 1 transição visual.

A prioridade é obter um pequeno ciclo jogável de ponta a ponta antes de expandir o conteúdo.

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

## Status

**Fase atual:** Fundação e arquitetura.

O próximo objetivo é estabelecer a documentação técnica e de design e, em seguida, construir o primeiro protótipo jogável.

---

*T.E.C.H. Digital — um RPG narrativo com regras próprias, mundo persistente e múltiplas perspectivas.*
