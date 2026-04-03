# video-examples

Companion code repo for the [Wired](https://youtube.com/@noxcraftdev) YouTube series.
noxcraftdev identity -- use `git@github-noxcraft:noxcraftdev/video-examples.git`.

## Series structure

All episodes live under `wired/`:

```
wired/
  e0-this-video-made-itself/
  e1-pipeline-upgrade/
  e2-hidden-statusbar/
  eN-slug/              ← next episode goes here
```

Folder naming: `eN-` prefix + kebab-case slug matching the video title.

## Adding a new episode

1. Create `wired/eN-slug/` with:
   - `README.md` -- what the episode covers, setup steps, usage
   - runnable code (scripts, configs, or both)
   - `requirements.txt` if Python deps are needed

2. Update `wired/README.md` -- add a row to the episode table.

3. Update root `README.md` -- add the same row to the Wired table.

4. Commit: `feat: add wired E<N> example -- <title>`

## Episode README template

```markdown
# eN-slug

Example from **Wired E<N>** by [@noxcraftdev](https://github.com/noxcraftdev):
*<Video title>*.

<One sentence on what the example does.>

## Files

- `script.py` -- <what it does>

## Setup / Usage

...
```

## What belongs here vs. self-funding/video-poc

- `video-poc/` -- internal production scripts (hardcoded paths, voice samples, raw pipeline)
- `video-examples/` -- clean, runnable versions for viewers (no hardcoded paths, generic CLI args)

When adapting from `video-poc`, remove path hardcoding and add `argparse`.
