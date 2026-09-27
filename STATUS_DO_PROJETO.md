# T.E.C.H. Digital - Status do Projeto

Atualizado em 27/09/2026.

## Objetivo atual

Construir um RPG digital com combate baseado em decisoes do jogador, rolagens de d20, fadiga, dano e respostas dos inimigos. A apresentacao usa uma tela de batalha inspirada nos RPGs classicos, com o personagem no canto inferior esquerdo e o inimigo no canto superior direito.

## O que ja funciona

- Ponte Python entre a RPG Engine e o Godot.
- Criacao e carregamento do personagem principal.
- Ataque basico com d20, alvo, dano e fadiga.
- Defesa com bonus temporario contra a resposta do inimigo.
- Golpe forte com dano maior, bonus de ataque e custo maior de fadiga.
- Recuperacao de fadiga limitada ao maximo do personagem.
- Resposta automatica do inimigo depois da acao do jogador.
- Condicoes de vitoria e derrota.
- Dois perfis de inimigo:
  - Alvo de treino.
  - Saqueador.
- Rodadas de combate e historico das ultimas acoes.
- Salvamento e carregamento do combate no Godot.
- Animacao visual simples do d20, mantendo o resultado real vindo da engine.
- Rolagem de iniciativa entre heroi e inimigo, com desempate a favor do heroi.
- Remocao completa da acao Mover, da distancia, do alcance e do minimapa.
- Tela inicial com titulo T.E.C.H. e fundos visuais.
- Tela de batalha com personagem, inimigo, barras de vida e fadiga.

## Arquivos principais

- `engine/rpg/bridge.py`
  - Entrada da comunicacao com o Godot.
  - Acoes de ataque, defesa, golpe forte, recuperacao e iniciativa.
  - Perfis de inimigos e serializacao dos resultados em JSON.
- `engine/rpg/combat/actions.py`
  - Definicoes das acoes e seus modificadores.
- `engine/rpg/combat/basic_actions.py`
  - Resolucao das acoes defensivas basicas.
- `godot/tech-digital/main.gd`
  - Interface, botoes, animacoes, historico e salvamento.
- `godot/tech-digital/main.tscn`
  - Layout da tela inicial e da tela de batalha.
- `godot/tech-digital/assets/`
  - Imagens usadas na tela inicial e no fundo da batalha.
- `engine/rpg/core/test_bridge_combat.py`
  - Testes do fluxo principal de combate e iniciativa.
- `engine/rpg/core/test_combat_balance.py`
  - Testes de balanceamento entre acoes e inimigos.

## Validacao atual

Comando usado:

```text
python -m unittest discover -s engine\rpg -p 'test_*.py'
```

Resultado atual: **12 testes aprovados**.

Tambem foi executado o `compileall` da engine Python e a verificacao de diferencas do Git, sem erros funcionais.

## Proximo passo recomendado

Conectar a iniciativa a ordem real dos turnos:

1. Rolar iniciativa uma vez no inicio do combate.
2. Mostrar os dois resultados no Godot.
3. Fazer quem venceu agir primeiro.
4. Impedir acoes fora do turno.
5. Salvar e restaurar o turno atual.

Depois disso, os proximos blocos sao efeitos de combate, equipamentos, inimigos com comportamentos diferentes e recompensas.

## Observacoes importantes

- A animacao atual do dado e visual; o resultado verdadeiro continua sendo calculado pela Python RPG Engine.
- O Godot nao foi executado neste ambiente porque o executavel nao esta disponivel aqui. A validacao visual final deve ser feita abrindo `godot/tech-digital/main.tscn` no Godot.
- A iniciativa ja e calculada e exibida, mas a ordem efetiva dos turnos ainda precisa ser conectada ao fluxo de acoes.
- Nenhum commit novo foi criado nesta sessao.
- O `.gitignore` e a remocao dos arquivos `__pycache__`/`.pyc` continuam preparados no estado atual do Git.

## Estado do Git no encerramento

Ha alteracoes staged relacionadas a limpeza do Python:

- `.gitignore` adicionado.
- Arquivos `__pycache__`/`.pyc` removidos do versionamento.

Ha tambem alteracoes de combate e Godot ainda nao commitadas:

- Ponte e regras de combate.
- Interface e cena do Godot.
- Testes automatizados.
- Assets visuais.

Antes do commit, revisar `git diff` e `git status`. Um nome sugerido para o commit e:

```text
Complete combat loop and clean Python generated files
```
