# Regras Provisórias

Este documento define como o T.E.C.H. Digital deve lidar com regras que ainda
não foram validadas pelo autor do T.E.C.H. RPG.

## Princípio

O desenvolvimento do jogo não deve ficar bloqueado enquanto uma regra estiver
pendente. Podemos usar valores provisórios, desde que eles sejam:

- explicitamente marcados como provisórios;
- centralizados em um único ponto de configuração;
- fáceis de substituir;
- nunca apresentados como regra oficial do T.E.C.H. RPG.

## Valores provisórios atuais

Em `engine/rpg/combat/rules.py`:

- ataque padrão: 10;
- defesa padrão: 10;
- dano padrão: 5.

Esses números existem apenas para permitir o desenvolvimento e os testes do
motor. Eles não representam uma decisão definitiva do sistema.

## Valores já confirmados

Também ficam centralizados nesse arquivo alguns valores que já foram
registrados como confirmados no material do projeto, como:

- Ataque Cirúrgico: +3 ataque e +3 dano;
- Lutar Defensivamente: -3 ataque e +1 defesa;
- Postura Defensiva: +4 defesa;
- Esquiva: custo de 3 Vel/Tur;
- Bloqueio: custo de 3 Vel/Tur;
- 1 Vel/Tur = 1,5 m;
- ação dedicada a movimento = 3 m.

## Regra de manutenção

Quando o autor validar uma regra pendente:

1. registrar a decisão no documento correspondente de game design;
2. substituir o valor provisório ou implementar a fórmula oficial;
3. atualizar os testes afetados;
4. remover a marca de provisório;
5. preservar compatibilidade dos saves quando necessário.

## O que não devemos fazer

Não devemos transformar uma hipótese temporária em regra permanente apenas
porque o protótipo depende dela.

Especialmente:

- não inventar fórmulas universais de ataque;
- não inventar fórmulas universais de defesa;
- não inventar redução de dano por armadura;
- não inventar tabelas de Ataque Múltiplo;
- não inventar regras de crítico além das que já foram confirmadas.

O motor deve permitir que essas regras sejam adicionadas posteriormente.
