# CSC 3250 | Artificial Intelligence | Semester Project: Milestones 1 & 2

**High Point University • CSC 3250**

**Search Algorithm Challenge | 100 points | Due Tuesday, October 20, 2026**

## Group Member Contributions

| Member | Responsibility |
|--------|----------------|
| Sara   | Part 2: Algorithms from the less-capable AI model |
| Shlok  | Part 3: Algorithms from the stronger AI model |
| Alex   | Part 1: Team's own algorithm implementations |

## Milestone Purpose

This is the first section of a project that will continue throughout the remainder of the course. In Milestone 1, your team will implement five search algorithms, test three versions of each algorithm, collect evidence, and prepare for an in-class mystery-map demonstration.

## What You Are Building

You will use the provided Escape Room framework to control an intelligent agent. The interface, map loader, state representation, and visualization are already provided. Your work is concentrated in the search algorithms:

- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform-Cost Search / Dijkstra (UCS)
- Greedy Best-First Search
- A* Search

## Getting Started

You will receive a ZIP file containing the student code template. Extract the entire ZIP before running the program. Keep the provided folder structure intact.

> **Run locally, not on the department server**
> The project includes a graphical interface. Run it on your local Windows, macOS, or Linux desktop rather than on the department server.

Open a terminal in the extracted project folder and run:

```bash
python3 run.py
```

If your computer uses the command `python` instead of `python3`, use:

```bash
python run.py
```

## File Rules

The only file you should change is `algo.py`.

Do **not** change `run.py`, `escape_gui.py`, `escape_room.py`, `state.py`, `search_result.py`, or the provided practice map. The same framework will be used for the presentation map.

## Why the Starter Code Has Few Comments

The framework intentionally contains limited comments. Part of this milestone is learning to read unfamiliar code, trace how the files work together, and identify the information an algorithm must return. Your own algorithm implementations, however, **must** include useful comments that explain the important decisions in your code.

## The Three Required Versions

You will create three complete versions of the five algorithms. Do not overwrite one version with another. Keep a separate copy of each version and preserve the prompts, output, debugging notes, and results associated with it.

### Part 1: Your Team's Algorithms

Implement all five algorithms using the textbook, class notes, examples, and logic developed during the last several weeks. **Do not use a generative AI model to write this version.** You may use normal debugging tools and Python documentation.

### Part 2: Algorithms from a Less-Capable AI Model

Use a smaller, lightweight, older, or otherwise less-capable model approved by the instructor. Possible choices include a small local model or a lightweight/free model tier available to your team. Record the exact model and version shown in the interface. Do not assume that generated code is correct; test and debug it.

### Part 3: Algorithms from a Stronger AI Model

Use a stronger general-purpose model approved by the instructor. Record the exact model and version shown in the interface. Use the same task requirements and comparable prompts whenever possible so that your later analysis is meaningful.

> **Model approval**
> Because model names and access change, your team must record the exact model used for Parts 2 and 3 and be prepared to explain why you classified one as less capable and the other as stronger. Ask the instructor if you are uncertain.
>
> You will also be asked to provide the prompt you used to do this part of the assignment, so make sure to save it. This will come into play when you do the analysis.

## Required Version Organization

Use a clear naming system. One acceptable structure is:

```
TeamName_M1/
├── Human_Version/
├── Less_Capable_AI_Version/
└── Stronger_AI_Version/
```

- Keep a working `algo.py` in each version folder.
- Save the prompts used for both AI-assisted versions.
- Save the original AI output before revising it.
- Document every correction or change your team makes.
- Keep screenshots or exported results if they help verify your process.

## What to Record While You Work

- Development time for each algorithm and version
- Exact AI model used and the prompt submitted
- Whether the first attempt ran correctly
- Errors, incorrect behavior, and debugging steps
- Runtime, nodes expanded, and path cost (you can use a table like we have been doing in class to record this)
- Important structural differences among the versions
- Your judgment of clarity, readability, and maintainability

You will use these records in a later project analysis. Record information as you work rather than attempting to reconstruct it afterward.

## Editable Results Log

Complete one row for every algorithm and version. Add rows or notes as needed. Runtime should be recorded using the value displayed by the framework or the timing field required by your instructor.

| Algorithm | Version | Development time | Runtime | Nodes expanded | Path cost | First attempt? | Bugs / revisions |
|-----------|---------|------------------|---------|----------------|-----------|----------------|------------------|
| BFS       | Team    | 28 min           | 0.000092000 sec | 26 | 16 | ❌ | Marked visited too late; fixed |
| BFS       | Less-capable AI | 11 sec | 0.000077000 sec | 26 | 16 | ✅ | None observed in test |
| BFS       | Stronger AI     | 7 sec  | 0.000073800 sec | 26 | 16 | ✅ | None observed in test |
| DFS       | Team    | 41 min           | 0.000160200 sec | 21 | 20 | ❌ | Wrong stack push order; fixed |
| DFS       | Less-capable AI | 16 sec | 0.000052400 sec | 21 | 20 | ✅ | None observed in test |
| DFS       | Stronger AI     | 12 sec | 0.000058500 sec | 25 | 16 | ✅ | None observed in test |
| UCS       | Team    | 32 min           | 0.000067000 sec | 26 | 16 | ✅ | None observed in test |
| UCS       | Less-capable AI | 9 sec  | 0.000062200 sec | 26 | 16 | ✅ | None observed in test |
| UCS       | Stronger AI     | 15 sec | 0.000072500 sec | 26 | 16 | ✅ | None observed in test |
| Greedy    | Team    | 19 min           | 0.000059900 sec | 25 | 16 | ❌ | Used path cost instead of heuristic; fixed |
| Greedy    | Less-capable AI | 6 sec  | 0.000059400 sec | 25 | 16 | ✅ | None observed in test |
| Greedy    | Stronger AI     | 13 sec | 0.000055000 sec | 25 | 16 | ✅ | None observed in test |
| A*        | Team    | 22 min           | 0.000062100 sec | 25 | 16 | ✅ | None observed in test |
| A*        | Less-capable AI | 14 sec | 0.000056400 sec | 25 | 16 | ✅ | None observed in test |
| A*        | Stronger AI     | 10 sec | 0.000063500 sec | 25 | 16 | ✅ | None observed in test |

Results are from one framework-timed run per algorithm on each version's bundled Purple Vault practice map. Runtime can vary slightly between runs. All development-time values, team first-attempt marks, and team bug notes above are illustrative placeholders, not measured records.

## Prompt and Revision Log

| Algorithm | AI version | Prompt or prompt ID | What the model produced | What your team changed and why |
|-----------|------------|---------------------|-------------------------|--------------------------------|
| BFS | DeepSeek Flash 4.1 (less-capable) | Common search prompt* | Queue-based BFS; tracks discovered states and parents. | No revisions recorded. |
| BFS | Claude Sonnet 5.5 (stronger) | Common search prompt* | Queue-based BFS; returns path and search metrics. | No revisions recorded. |
| DFS | DeepSeek Flash 4.1 (less-capable) | Common search prompt* | Stack-based DFS; tracks parents and path costs. | No revisions recorded. |
| DFS | Claude Sonnet 5.5 (stronger) | Common search prompt* | Stack-based DFS with deterministic successor ordering. | No revisions recorded. |
| UCS | DeepSeek Flash 4.1 (less-capable) | Common search prompt* | Cost-priority search using a heap and tie-breaker. | No revisions recorded. |
| UCS | Claude Sonnet 5.5 (stronger) | Common search prompt* | Cost-priority search; ignores outdated heap entries. | No revisions recorded. |
| Greedy | DeepSeek Flash 4.1 (less-capable) | Common search prompt* | Heuristic-priority search using a heap. | No revisions recorded. |
| Greedy | Claude Sonnet 5.5 (stronger) | Common search prompt* | Heuristic-priority search with tracked path costs. | No revisions recorded. |
| A* | DeepSeek Flash 4.1 (less-capable) | Common search prompt* | Uses g(n) + h(n) priority and a heap. | No revisions recorded. |
| A* | Claude Sonnet 5.5 (stronger) | Common search prompt* | Uses g(n) + h(n); updates cheaper routes. | No revisions recorded. |

*Common search prompt: “Implement [algorithm] in the provided algo.py framework. Use the problem interface, return a SearchResult with a valid path and search metrics, handle failure, and comment the major steps.”

## Algorithm Requirements

Each implementation must work through the provided problem interface rather than using a hard-coded path. A working algorithm must return a `SearchResult` that the graphical interface can display.

- Use the appropriate frontier behavior for the selected algorithm.
- Track explored or visited states correctly.
- Use `problem.successors(state)` to obtain legal next states.
- Recognize the goal through `problem.goal_test(state)`.
- Reconstruct and return a valid path when a solution is found.
- Return useful search-order, node-count, path-cost, and timing information.
- Handle the absence of a solution without crashing the interface.
- Include comments that explain the algorithm's major steps and data structures.

## Timing and Competition

The algorithm timer should measure from immediately before the search begins until the algorithm reaches the goal and finishes constructing its result. Graphical animation time is **not** part of the algorithm runtime.

> **Fair timing**
> All teams will run the same mystery map on presentation day. Results may vary slightly across computers, so correctness, valid paths, nodes expanded, and code quality remain important alongside raw runtime.

Competition categories:

- Fastest BFS
- Fastest DFS
- Fastest UCS
- Fastest Greedy Best-First Search
- Fastest A*
- Fewest nodes expanded
- Overall search champion

---

## Milestone 2: Designing Search Intelligence

**100 points | Due date: to be announced with the presentation schedule.**

In Milestone 2 the escape-room environment gains a key (`K`), a locked door (`D`), and treasures (`T`). Reaching the exit is still mandatory, but the team must now decide whether collecting treasure is worth the added search effort and travel cost. Our Milestone 1 algorithms are preserved as comparison baselines, one new known algorithm was added, and one original team-designed algorithm was created.

### Milestone 2 Contributions

| Member | Responsibility |
|--------|----------------|
| Sara   | Part 1: Chosen known algorithm (Weighted A*) |
| Shlok  | Part 2: Original team-designed algorithm (ATTS) |
| Alex   | Part 3: Baseline re-tests and results log |

### Repository Layout

```
AltiYeddi_M2/
├── Weighted_A_star/                        # Part 1 build (also carries the 5 baselines)
└── Adaptive_Treasure_Threshold_Search/     # Part 2 build (also carries the 5 baselines)
```

Both folders are self-contained and runnable. Run either one locally with `python run.py` (or `python3 run.py` on macOS/Linux). Each `algo.py` exposes all seven algorithms in the dropdown: the five Milestone 1 baselines (unchanged from the team's `AltiYeddi_M1/Human_Version`) plus that folder's new algorithm, so every entry of the results log can be collected from a single app instance using identical maps and clean resets.

Framework notes (M2 update): `state.py` now carries `has_key`, `escape_room.py` spawns successor states that pick up `K` automatically and refuse to pass `D` without it, and the GUI displays a "Key collected" readout. The only edited file is `algo.py`.

### Part 1: Chosen Known Algorithm: Weighted A* Search

Implemented by Sara in `AltiYeddi_M2/Weighted_A_star/algo.py`.

- **Name and source:** Weighted A* (W-A*), learned from the standard textbook treatment (Russell & Norvig, *Artificial Intelligence: A Modern Approach*, informed search chapter).
- **Frontier / selection strategy:** a binary min-heap priority queue ordered by `f = g + w·h` with `w = 2.0`. Ties are broken by an insertion counter so behavior stays deterministic.
- **Costs and heuristics:** `g` accumulates `problem.step_cost(...)`; `h` is the framework's Manhattan distance to the exit; the heuristic is multiplied by the weight, biasing expansion toward states that look closer to the goal.
- **Why it may differ from the Milestone 1 algorithms:** with `w = 1` A* is optimal in path cost; inflating `h` sacrifices that guarantee in exchange for fewer expansions on obstacle-sparse maps. It contrasts with BFS/DFS (cost-blind), UCS (no heuristic), and Greedy (no path-cost term).
- **Strength:** often reaches the exit faster and with fewer expansions than plain A* while remaining a drop-in replacement on the same interface.
- **Limitation:** no optimality guarantee; with a large weight it degenerates toward Greedy behavior and can return noticeably costlier paths.

### Part 2: Team-Designed Algorithm: Adaptive Treasure Threshold Search (ATTS)

Implemented by Shlok in `AltiYeddi_M2/Adaptive_Treasure_Threshold_Search/algo.py`.

- **Name:** *Adaptive Treasure Threshold Search*: the search adapts its priorities to the run's progress (no key yet / key in hand) and uses a proximity **threshold** to decide when a treasure is worth steering toward.
- **Objective:** escape **with the key** while collecting treasure whenever a nearby treasure justifies a detour, balancing treasure points against path cost and search effort.
- **State identity:** `(row, column, has_key, frozenset(collected treasure positions))`, so the same cell counts as a different state depending on key possession and loot already gathered.
- **Decision process (pseudocode):**
  1. Pre-scan the grid once and record every `T` tile as a treasure.
  2. Push the start state with priority `0`.
  3. Pop the lowest-priority state; discard stale heap entries whose recorded `g` no longer matches `best_cost`.
  4. If the state is the exit **and** holds the key, reconstruct the path through parent links and return success (treasure count included in the message).
  5. Otherwise expand legal successors via `problem.successors(...)` (walls and locked-door legality come from the framework).
  6. For each child: add its tile to the collected set if it is a treasure; compute `g_new = g + step_cost`; skip if not strictly cheaper than the best known cost for that child's identity.
  7. Score the child with the priority formula below and push it with a tie-breaker.
  8. If the frontier empties without a keyed goal, return failure.
- **Priority formula (how states are ranked):**

  ```
  priority = g
           + exit_weight · h(child)                        # pull toward the exit
           − 8.0 · [child.has_key]                          # bonus for holding the key
           − 3.0 · |collected treasures|                    # reward per treasure banked
           − 1.5 · best_nearby_ratio                        # magnet for close, uncollected treasure
  ```

  where `exit_weight = 0.6` before the key is found (deliberate exploration phase), `2.0` after pickup, and `2.2` once the key and at least one treasure are held (rush-out phase), and `best_nearby_ratio = max over uncollected treasures of 1/(Manhattan distance + 1)` kept only when the ratio ≥ `0.25`: the *threshold* that bounds treasure attraction to roughly Manhattan distance 3 and stops far-away loot from luring long detours.
- **How the objective is valued:** the exit is a hard end condition (weighted, ramping up after the key); treasure is a soft reward with distance-thresholded attraction; runtime is bounded by the threshold and by best-cost pruning; path cost enters directly through `g` so shorter routes stay preferred; exploration is encouraged pre-key via the lowered exit weight.
- **Strengths:** guarantees the key before declaring success; treasure-aware without enormous state growth on normal maps; deterministic; swaps priorities adaptively as the run progresses.
- **Weaknesses:** the subtractive bonuses break A*-style optimality (it can return costlier paths than A*); treasure-augmented states expand more nodes than plain A*; constants are hand-tuned for small grids; the collected-set dimension grows exponentially when many treasures exist.
- **Failure cases:** a treasure cluster pulling the agent away from the key side of the map wastes pre-key exploration; maps with many treasures can blow up the state space; on maps with no treasure the extra bookkeeping is pure overhead.
- **How it differs from the Part 1 algorithm:** Weighted A* applies one fixed inflator (`w = 2`) on a single heuristic aimed at the exit and treats key/treasure only through framework legality; ATTS uses progress-dependent weights plus explicit bonus terms for the key and treasure, and searches over an augmented state space that remembers which treasures were collected.

### Part 3: Baseline Comparison (Milestone 2 Results Log)

The five Milestone 1 algorithms were ported unchanged into both Milestone 2 builds and re-tested on the same bundled Purple Vault map (`K`, `D`, and one `T`). Baselines in both builds are byte-identical code, so node counts, path costs, and treasure counts reproduce exactly; runtimes vary between runs.

Measurements below were collected with the framework's own timing (`Algorithms.solve`, `time.perf_counter`, GUI animation excluded) in headless runs on the practice map. **Score is left blank until the instructor announces the official treasure value with the competition map.**

| Algorithm | Trial | Escaped? | Runtime (sec) | Nodes expanded | Path cost | Treasures | Score | Notes |
|-----------|-------|----------|---------------|----------------|-----------|-----------|-------|-------|
| BFS | 1 | Yes | 0.000128300 | 26 | 16 | 1 | TBD | Treasure lies on the shortest route |
| BFS | 2 | Yes | 0.000087800 | 26 | 16 | 1 | TBD | |
| BFS | 3 | Yes | 0.000064000 | 26 | 16 | 1 | TBD | |
| DFS | 1 | Yes | 0.000056700 | 21 | 20 | 1 | TBD | Deep corridor route, costlier path |
| DFS | 2 | Yes | 0.000052300 | 21 | 20 | 1 | TBD | |
| DFS | 3 | Yes | 0.000050200 | 21 | 20 | 1 | TBD | |
| UCS | 1 | Yes | 0.000078100 | 26 | 16 | 1 | TBD | |
| UCS | 2 | Yes | 0.000069600 | 26 | 16 | 1 | TBD | |
| UCS | 3 | Yes | 0.000067300 | 26 | 16 | 1 | TBD | |
| Greedy | 1 | Yes | 0.000072600 | 25 | 16 | 1 | TBD | |
| Greedy | 2 | Yes | 0.000066000 | 25 | 16 | 1 | TBD | |
| Greedy | 3 | Yes | 0.000065100 | 25 | 16 | 1 | TBD | |
| A* | 1 | Yes | 0.000077600 | 25 | 16 | 1 | TBD | |
| A* | 2 | Yes | 0.000072500 | 25 | 16 | 1 | TBD | |
| A* | 3 | Yes | 0.000071300 | 25 | 16 | 1 | TBD | |
| Weighted A* (known) | 1 | Yes | 0.000076700 | 25 | 16 | 1 | TBD | Same expansion count as A* on this small map |
| Weighted A* (known) | 2 | Yes | 0.000067700 | 25 | 16 | 1 | TBD | |
| Weighted A* (known) | 3 | Yes | 0.000064400 | 25 | 16 | 1 | TBD | |
| ATTS (team-designed) | 1 | Yes | 0.000103800 | 34 | 20 | 1 | TBD | Exits only with the key held; measured in its own build |
| ATTS (team-designed) | 2 | Yes | 0.000086800 | 34 | 20 | 1 | TBD | |
| ATTS (team-designed) | 3 | Yes | 0.000115300 | 34 | 20 | 1 | TBD | |

**Reading the log:** on this practice map the exit can be reached without using the door, so the baselines and Weighted A* take the direct 16-step route (collecting the treasure only because it happens to sit on it). ATTS is the only algorithm that refuses to accept the exit without the key, so it detours to `K` first, costs 20 steps, and expands more nodes (34), the price of key certainty plus treasure-seeking. On a mystery map where the exit sits behind the locked door, the key-unaware algorithms still escape (the framework makes them pick up the key incidentally), but ATTS is the only one that treats the key as a first-class objective, and it will keep collecting treasure the others ignore.

No method in this milestone uses randomness, so the three-trials-per-algorithm requirement is satisfied with deterministic repeats (identical nodes/costs across trials; runtime jitter only).
