# AGENTS.md — Sistema Operacional Profissional Codex

Este projeto utiliza um fluxo profissional com Codex focado em previsibilidade, segurança e entrega contínua.

## Estrutura oficial (organizada)

- `AGENTS.md` fica na **raiz**.
- Todo o restante do kit fica em `.codex-kit/`:
  - `.codex-kit/agents/`
  - `.codex-kit/skills/`
  - `.codex-kit/templates/`
  - `.codex-kit/docs/` (opcional)

## Regras obrigatórias (gates)

1. Não implementar sem design aprovado.
2. Não iniciar sem plano executável por tarefas atômicas.
3. Não concluir sem validação técnica registrada.
4. Não concluir sem code review.
5. Não marcar "done" sem verificação final.

## Diretriz de saída de código

- Quando pedir implementação, solicite **apenas código**.
- Use: `Only output code. Do not add comments or explanations.`
- Evite respostas verbosas em tarefas de geração direta.
- Explicações só quando você pedir explicitamente.

## Roteador de skills: qual usar em cada situação

### 1) Ideia vaga / escopo confuso
- Use: `.codex-kit/skills/brainstorming/`
- Resultado esperado: design objetivo e escopo fechado.

### 2) Design aprovado e precisa executar com qualidade
- Use: `.codex-kit/skills/writing-plans/`
- Resultado esperado: plano com tarefas de 5–15 min, arquivos-alvo e validação por tarefa.

### 3) Execução normal com checkpoints
- Use: `.codex-kit/skills/executing-plans/`
- Resultado esperado: implementação incremental, uma tarefa por vez.

### 4) Execução com subagentes/revisão em cadeia
- Use: `.codex-kit/skills/subagent-driven-development/`
- Resultado esperado: implementação com revisão de conformidade + qualidade.

### 5) Lógica crítica ou com risco de regressão
- Use: `.codex-kit/skills/test-driven-development/`
- Resultado esperado: ciclo RED-GREEN-REFACTOR.

### 6) Bug difícil / comportamento inconsistente
- Use: `.codex-kit/skills/systematic-debugging/`
- Resultado esperado: causa raiz identificada + correção validada.

### 7) Antes de fechar qualquer tarefa importante
- Use: `.codex-kit/skills/requesting-code-review/`
- Apoio: `.codex-kit/agents/code-reviewer.md`
- Resultado esperado: findings por severidade + correções.

### 8) Recebeu feedback e precisa responder com maturidade
- Use: `.codex-kit/skills/receiving-code-review/`
- Resultado esperado: resposta técnica clara + correções rastreáveis.

### 9) Finalização e evidência de conclusão
- Use: `.codex-kit/skills/verification-before-completion/`
- Resultado esperado: checklist objetivo + evidências executáveis.

### 10) Organização de branches paralelas
- Use: `.codex-kit/skills/using-git-worktrees/`
- Resultado esperado: isolamento seguro entre frentes.

### 11) Encerramento de branch
- Use: `.codex-kit/skills/finishing-a-development-branch/`
- Resultado esperado: decisão de merge/PR com validação final.

### 12) Quando houver trabalho de UI/UX
- Use: `.codex-kit/skills/ui-ux-pro-max/`
- Resultado esperado: direção visual + tokens + checklist de acessibilidade + validação responsiva.

## Fluxo operacional

1. Brainstorm/design
2. Plano executável
3. Execução por tarefa
4. Code review
5. Verificação final
6. Encerramento de branch

## Segurança mínima obrigatória

- Nunca commitar segredos (`.env`, chaves, tokens).
- Sempre revisar scripts antes de `chmod +x` e execução.
- Em dúvida entre velocidade e segurança, escolher segurança.