# IEL: Intent-Level Experience Learning

Code for the paper **IEL: Intent-Level Experience Learning for LLM-based Customer Service Agents**. The method is non-parametric: the executor LLM's weights are never updated; completed episodes are turned into an external, intent-indexed library of procedures that is routed back to later requests. See the paper for the method.

---

## Setup

Python 3.10+ (developed on 3.12).

```bash
pip install -r requirements.txt
```

Models are called through the **OpenAI-compatible chat completions API**, so any provider that speaks it works. Create `.env` in the repository root:

```bash
# The agent under test (also used by IEL's own decomposition / induction calls)
AGENT_LLM_BASE_URL=https://...
AGENT_LLM_API_KEY=sk-...
AGENT_LLM_MODEL=...

# The simulated user
USER_LLM_BASE_URL=https://...
USER_LLM_API_KEY=sk-...
USER_LLM_MODEL=...

# Vision model behind the get_image_info tool (used by the `story` dataset only)
VLM_BASE_URL=...
VLM_API_KEY=...
VLM_MODEL=...
```

`--agent-model` / `--user-model` override the `*_MODEL` defaults; the base URL and API key always come from `.env`. `.env` is gitignored.

### Datasets

| `--env` | Dataset | Tasks | Domain |
|---|---|---|---|
| `story` | ECom-Bench | 53 | Home appliances |
| `xcat` | ECom-Bench-XCAT | 60 | Clothing + food |

### Methods

| `--agent-impl` | Method |
|---|---|
| `official` | ReAct baseline (the ECom-Bench executor) |
| `intent` | IEL (ours) |

---

## Run

One script per experiment — dataset × method. Each runs the whole flow once, from a cold start to a `pass^k` report, with no manual steps in between:

| Command | Experiment |
|---|---|
| `bash scripts/run_story_iel.sh` | ECom-Bench × IEL |
| `bash scripts/run_story_react.sh` | ECom-Bench × ReAct |
| `bash scripts/run_xcat_iel.sh` | ECom-Bench-XCAT × IEL |
| `bash scripts/run_xcat_react.sh` | ECom-Bench-XCAT × ReAct |

IEL additionally grows an experience library before it evaluates, so its scripts take noticeably longer. The full rationale for every step is in the header comment of the script itself.

Each script:

1. **Grows** *(IEL only)* — from an empty directory, builds an experience library on the other folds and freezes it as a snapshot.
2. **Audits and leak-checks** *(IEL only)* — gates the frozen taxonomy, then verifies the snapshot holds no episode from the test fold.
3. **Evaluates** — mounts the snapshot read-only (`--evolve false`) and evaluates the chosen method on the held-out fold, 3 trials per task.
4. **Reports** — `pass^k` (k = 1, 2, 3) per fold and across folds, per-dimension failure counts, and token cost.

Everything lands under `results/<dataset>/<method>/`, with one log per invocation.

```bash
# Single task, no folds — a quick smoke test
python run.py --env story --inject true --evolve true --task-ids 0 1

# Both methods on one dataset, for the paired comparison
bash scripts/run_story_react.sh && bash scripts/run_story_iel.sh
```

### Knobs

Every knob is an environment variable with a working default; see the header of any script.

```bash
RUN_NUM_TRIALS=1  bash scripts/run_xcat_iel.sh   # cheaper run (only pass^1 meaningful)
RUN_CONCURRENCY=20 bash scripts/run_xcat_iel.sh  # more parallel evaluation
RUN_PYTHON=/path/to/python bash scripts/run_story_iel.sh
```

### Folds

`folds/<dataset>_3fold_seed10.json` holds the cross-validation split (committed). Inspect one, or generate a new split:

```bash
python -m folds show --spec folds/xcat_3fold_seed10.json
python scripts/make_folds.py --env xcat --k 3 --seed 11   # a new seed -> a new scheme
```

`make_folds.py` refuses to overwrite an existing scheme file, since a scheme that produced results is part of those results.

### Gotchas

- Evaluating a test fold with `--evolve true` is training on the test set. `run.py` refuses to start on that combination.
- A snapshot directory is never overwritten: the numbers would no longer say which library they came from. Delete it deliberately if you mean to redo that round.

---

## Repository structure

```
intent/                the method
  decomposer.py          turn-level intent decomposition + taxonomy matching
  verifier.py            shared verifier: negative-signal / repeated-question judgement
  instances.py           cross-turn instance reconstruction + tool-call attribution
  outcome.py             trajectory-derived outcome labels
  ledger.py              candidate accumulator with evidence gates
  adjudicator.py         merge / new / defer resolution + periodic merge scan
  distiller.py           procedure induction from verified instances
  taxonomy.py            taxonomy load/save, aliases, slot schemas
  store.py               instance / experience / evolution-log persistence
  jsonio.py              tolerant parsing of LLM structured output
  pipeline.py            the episode-level write path
  snapshot.py            library snapshot + leak-safe frozen evaluation
  stats.py, usage.py     mechanism metrics, token accounting
  prompts.py, config.py  prompt material and all tunable constants
  eval_decomposition.py  offline decomposition scoring

envs/                  datasets + the single environment implementation
  env.py                 ToolUseEnv — the shared tool-use environment
  dataset.py             Dataset = tasks + system prompt + offline store
  base.py                Env ABC
  story/                 ECom-Bench: tasks.py, wiki.md, data/
  xcat/                  ECom-Bench-XCAT: tasks.py, wiki.md, data/

agent/                 executors
  agents_list/agent_official.py   ReAct baseline
  agents_list/agent_langchain.py  IEL's intent-aware executor
  servers/offline/                the mock e-commerce tool server (MCP)

user/                  simulated user
folds/                 cross-validation split specs (one per dataset)
scripts/               one runnable flow script per experiment, plus make_folds.py
wikis/                 agent-side system prompt

run.py                 CLI entry point; main.py drives a batch
utils.py               executor, injection and token accounting
llm_config.py          role -> provider credentials from .env
```
