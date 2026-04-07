# Autonomous Git Bisect with Claude Code

Find which commit broke your tests without touching the keyboard.

## The prompt

```
Find which commit broke this test: `cargo test test_auth_flow`

Use git bisect. The last known good commit is abc1234 (Tuesday).
HEAD is bad. Run the test at each step and mark good/bad automatically.
When you find the culprit, show me the diff and explain why it broke.
```

## How it works

1. Claude starts `git bisect start`
2. Marks the known good and bad commits
3. At each bisect step: checks out the commit, runs the test, marks good/bad
4. Binary search narrows 30 commits to 1 in ~5 steps
5. Shows the breaking commit's diff and explains the root cause

## Tips

- Always specify the test command explicitly
- Provide the last known good commit (or "last Tuesday" -- Claude will find it via `git log`)
- Works with any test runner: cargo test, pytest, jest, go test
