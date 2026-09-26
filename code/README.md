# code/

Every listing, lab, measurement and plot in *Chaos from Zero*, as one
[uv](https://docs.astral.sh/uv/) project locked to the versions printed on
the book's copyright page.

```bash
uv sync --locked                        # the environment, exactly as CI has it
uv run python ch05/four_rates.py        # run any listing the book prints
uv run pytest -k l05_01                 # check your answer to Lab 5.1
CHAOS_SOLUTIONS=1 uv run pytest         # what CI runs: every listing, every solution
CHAOS_STARTERS=fail uv run pytest labs  # every starter must still FAIL its test
```

| Directory | What is in it |
|---|---|
| `src/chaoslab/` | The small library the book's listings share: iteration, integrators, the systems, the measurements |
| `chNN/` | The listings of chapter NN, each a script that CI runs |
| `labs/chNN/` | Lab starters (yours to finish), `solutions/`, and the tests |
| `measure/` | The scripts that compute every number the book prints (`figures/values/`) and every console transcript (`figures/transcripts/`) |
| `plots/` | The scripts that draw every plot, once per language |

The labs start **failing on purpose**. Open the starter, read its docstring,
make the test pass. The reference solution is under `solutions/` and is there
so the build can prove every lab is solvable; look at it after, not before.
