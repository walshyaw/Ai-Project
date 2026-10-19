# CSC 3250 | Artificial Intelligence — Semester Project: Milestone 1

**High Point University • CSC 3250**

**Search Algorithm Challenge | 100 points | Due Tuesday, October 20, 2026**

## Group Member Contributions

| Member | Responsibility |
|--------|----------------|
| Sara   | Part 2 — Algorithms from the less-capable AI model |
| Shlok  | Part 3 — Algorithms from the stronger AI model |
| Alex   | Part 1 — Team's own algorithm implementations |

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
|           |            |                     |                         |                                |

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

## Presentation Day: Tuesday, October 20

Your team will receive a different map on presentation day. You will load that map into the provided framework and demonstrate each completed algorithm. **The map will not be released in advance.**

- Be ready to identify which version of the code you are demonstrating.
- Explain the frontier, visited-state handling, goal test, and path reconstruction.
- Show the recorded runtime, nodes expanded, and path cost.
- Be prepared to discuss one meaningful difference among the three versions.
- Every team member should be able to answer questions about the code.

## Submission Checklist

- [ ] All five algorithms are implemented in the team-created version.
- [ ] All five algorithms are generated and tested with a less-capable AI model.
- [ ] All five algorithms are generated and tested with a stronger AI model.
- [ ] The three versions are saved separately and clearly labeled.
- [ ] Prompts and original AI outputs are preserved.
- [ ] Runtime, nodes expanded, path cost, development time, and debugging notes are recorded.
- [ ] Your algorithm code includes useful comments.
- [ ] The program runs locally through `python3 run.py` or `python run.py`.
- [ ] The team is prepared for the mystery-map demonstration on October 20.

## Reminder

This is Milestone 1, not the complete semester project. The framework and algorithms will be extended as we study additional AI topics. Build and document this foundation carefully because your team will use it again.
