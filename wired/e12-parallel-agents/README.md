# Parallel Agents with Worktree Isolation

Spawn multiple Claude Code agents that work on the same repo simultaneously without merge conflicts.

## How it works

The `isolation: "worktree"` parameter gives each agent its own git worktree -- a separate working directory with its own branch, sharing the same git history as the main repo.

```
Agent(
    prompt="Implement the auth module",
    isolation="worktree",
    run_in_background=True,
)
```

## Example: Three parallel agents

In a single Claude Code message, spawn three agents with worktree isolation:

1. **Frontend agent** -- implements the UI components
2. **Backend agent** -- builds the API endpoints  
3. **Test agent** -- writes integration tests

Each agent gets its own worktree and branch. When done, merge the branches.

## Key details

- Worktrees are created in `.claude/worktrees/`
- Each gets a new branch based on HEAD
- Automatic cleanup if the agent makes no changes
- If changes are made, the worktree path and branch are returned
- No coordination needed between agents
