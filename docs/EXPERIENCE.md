# Experience Index

Flywheel experience artifacts are derived from observer JSON traces.

The index is intended to make repeated workflow facts visible: skipped validation, risks, follow-up work, action classes, and recommended next states.

## Why Use It?

Use the experience index when you want to learn from completed cycles instead of rereading individual observer reports.

Good uses:

- see how many observer traces exist
- spot repeated skipped validation
- count unresolved risks and follow-ups
- summarize action classes over time
- prepare evidence before changing prompts, hooks, or process docs

Do not use it as the source of truth for a cycle. Observer JSON traces remain the source; experience files are derived summaries.

## Quick Start

Refresh the index:

```bash
./flywheel/tools/flywheel_experience.sh index
```

Show aggregate metrics:

```bash
./flywheel/tools/flywheel_experience.sh summarize
```

Use JSON for automation:

```bash
./flywheel/tools/flywheel_experience.sh summarize --format json
```

## Location

Experience artifacts live under `experience.path` from `flywheel.yaml`.

Default:

```yaml
experience:
  path: "flywheel/artifacts/experience"
```

## Commands

Build or refresh the index:

```bash
./flywheel/tools/flywheel_experience.sh index
./flywheel/tools/flywheel_experience.sh index --format json
```

Summarize current traces:

```bash
./flywheel/tools/flywheel_experience.sh summarize
./flywheel/tools/flywheel_experience.sh summarize --format json
```

## Generated Files

The index command writes:

- `index.jsonl`: one compact record per observer trace
- `stage-metrics.json`: aggregate counts
- `lessons.md`: human-readable summary scaffold

These files are derived artifacts. Regenerate them with `flywheel_experience.sh index` after observer traces change.

## Source Data

The indexer reads JSON files from `paths.artifacts.observer`.

It does not mutate observer traces. It only writes derived artifacts under `experience.path`.

## Example Workflow

1. Close a cycle:

```bash
./flywheel/tools/run_observer_cycle.sh --cycle-id <cycle-id>
```

2. Refresh experience artifacts:

```bash
./flywheel/tools/flywheel_experience.sh index
```

3. Read the human summary:

```text
flywheel/artifacts/experience/lessons.md
```

4. Use the summary to decide whether a prompt, hook, or stage gate needs improvement.

## Current Limits

The first experience index implementation summarizes existing trace fields. It does not yet:

- query individual lessons by stage or risk
- infer root causes
- update prompts or docs automatically
- attach experience summaries to stage launch context
