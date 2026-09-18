# MASTER PROJECT PROMPT
## Build a Complete, Production-Quality Python + Streamlit Project
### Project: Building an Uncertainty-Aware Warehouse Robot Brain

You are a senior AI/ML/Python software architect and developer with 20+ years of practical experience in Python, artificial intelligence, machine learning, planning systems, probabilistic reasoning, game AI, neural networks, expert systems, testing, software architecture, and deployment.

I have an existing implementation of this project, but it is incomplete and/or not perfectly implemented.

Your job is to **inspect the existing project, compare it against the complete project specification below, identify every missing or incorrect requirement, and then rebuild/refactor the project into a clean, working, easily deployable application.**

Do NOT make a superficial demo.

The final implementation must actually execute the required algorithms and demonstrate their behavior.

The original project specification is the source of truth.

---

# 1. SOURCE-OF-TRUTH REQUIREMENT

The project is called:

**Building an Uncertainty-Aware Warehouse Robot Brain**

It is an integrated warehouse-robot intelligence system consisting of five modules:

1. Module A — Planning: Stack the Pallet
2. Module B — Reasoning Under Uncertainty: Is This Box Damaged?
3. Module C — Game Playing: Dock Contention
4. Module D — Connectionist Models: Anomaly Recall
5. Module E — Expert System: The Maintenance Advisor

These modules must also be integrated into one simulated warehouse control loop.

The original specification explicitly requires working code, correct behavior on test cases, and the ability to explain why the system made a decision.

Do not replace required algorithms with fake/random outputs.

---

# 2. FIRST TASK — AUDIT THE EXISTING PROJECT

Before changing code:

1. Inspect the complete repository.
2. Inspect every Python file.
3. Inspect every configuration file.
4. Inspect requirements/dependency files.
5. Inspect existing Streamlit pages/components.
6. Inspect existing models and datasets.
7. Inspect tests.
8. Inspect README/documentation.
9. Run the existing application if possible.
10. Run existing tests.
11. Identify runtime errors.
12. Identify logical errors.
13. Identify incomplete algorithms.
14. Identify requirements from the specification that are missing.
15. Identify requirements that are implemented incorrectly.
16. Identify duplicated or unnecessary code.

Create an internal implementation checklist mapping:

PDF requirement → existing implementation → status → required fix.

Do not delete working functionality unless there is a strong architectural reason.

Preserve useful existing code where possible, but correct it where necessary.

---

# 3. FINAL TECHNOLOGY STACK

Use:

- Python 3.10+
- Streamlit for the complete frontend
- NumPy
- pandas
- matplotlib
- scikit-fuzzy
- pgmpy OR another reliable Bayesian-network library
- PyTorch OR TensorFlow/Keras for the RNN
- standard Python libraries where practical

Prefer lightweight and stable dependencies.

Avoid unnecessary dependencies.

The application must be deployable on:

- Local machine
- Streamlit Community Cloud or equivalent simple cloud deployment

Provide:

requirements.txt

and, if useful:

runtime.txt

or an appropriate Python-version configuration.

---

# 4. REQUIRED PROJECT ARCHITECTURE

Create a clean structure similar to:

warehouse_robot_brain/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── config.py
│
├── modules/
│   ├── planning/
│   │   ├── __init__.py
│   │   ├── goal_stack.py
│   │   ├── nonlinear_planner.py
│   │   ├── hierarchical_planner.py
│   │   ├── reactive_planner.py
│   │   └── models.py
│   │
│   ├── uncertainty/
│   │   ├── __init__.py
│   │   ├── nonmonotonic.py
│   │   ├── bayesian.py
│   │   ├── certainty_factors.py
│   │   ├── bayesian_network.py
│   │   ├── dempster_shafer.py
│   │   ├── fuzzy_logic.py
│   │   └── comparison.py
│   │
│   ├── game/
│   │   ├── __init__.py
│   │   ├── game_state.py
│   │   ├── minimax.py
│   │   ├── alpha_beta.py
│   │   ├── iterative_deepening.py
│   │   └── visualization.py
│   │
│   ├── connectionist/
│   │   ├── __init__.py
│   │   ├── hopfield.py
│   │   ├── rnn.py
│   │   ├── dataset.py
│   │   └── comparison.py
│   │
│   ├── expert_system/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── rules.json
│   │   ├── knowledge_acquisition.py
│   │   └── explanations.py
│   │
│   └── integration/
│       ├── __init__.py
│       ├── control_loop.py
│       ├── simulation.py
│       └── shift_log.py
│
├── ui/
│   ├── overview.py
│   ├── planning_page.py
│   ├── uncertainty_page.py
│   ├── game_page.py
│   ├── connectionist_page.py
│   ├── expert_system_page.py
│   └── integration_page.py
│
├── data/
│   ├── sensor_data.csv
│   └── sample_shift_log.csv
│
└── tests/
    ├── test_planning.py
    ├── test_uncertainty.py
    ├── test_game.py
    ├── test_hopfield.py
    ├── test_rnn.py
    ├── test_expert_system.py
    └── test_integration.py

You may modify this structure if you have a better architecture, but keep the five modules clearly separated.

---

# 5. MODULE A — PLANNING: STACK THE PALLET

Implement a genuine Blocks World planner.

Use boxes:

A, B, C, D, E, F, G

The planner must support arbitrary start states and arbitrary goal states.

## A1. Goal Stack Planning

Implement classic Goal Stack Planning.

Input:

start state
goal state

Output:

- generated plan
- ordered actions
- execution trace
- intermediate states
- success/failure
- explanation of why each action was selected

Support primitive operations such as:

- PICKUP
- PUTDOWN
- STACK
- UNSTACK

The planner must actually reason about:

- On(x,y)
- OnTable(x)
- Clear(x)
- Holding(x)
- HandEmpty

Do not hard-code one single solution.

---

# 6. MODULE A2 — NONLINEAR / LEAST-COMMITMENT PLANNING

Implement a nonlinear planner using constraint posting / least commitment concepts.

It must work on the same Blocks World representation.

Represent:

- actions
- preconditions
- effects
- ordering constraints
- causal links where appropriate
- threats where appropriate

Demonstrate a scenario where nonlinear planning allows more flexible ordering and/or parallel-executable actions compared with Goal Stack Planning.

The UI must show:

Goal Stack result

versus

Nonlinear planner result

including:

- action count
- ordering constraints
- possible parallel actions
- explanation

Do not merely claim that the nonlinear planner is better.

Actually demonstrate the difference.

---

# 7. MODULE A3 — HIERARCHICAL PLANNING

Implement at least one high-level operator:

LoadPallet(P)

Expand it into primitive actions.

For example:

LoadPallet(P)
→ arrange boxes
→ pick up required box
→ stack required box
→ verify placement

The decomposition must be visible in the Streamlit UI.

Show:

High-level action

↓

Intermediate actions

↓

Primitive actions

---

# 8. MODULE A4 — REACTIVE PLANNING

Add a reactive layer.

During execution, simulate a random disturbance such as:

- box knocked over
- box moved unexpectedly
- box becomes unavailable
- stack becomes invalid

The robot must react using the current plan rather than blindly continuing.

The reactive system must:

1. Detect disturbance.
2. Identify affected state.
3. Repair/adjust the current plan.
4. Continue execution.
5. Log the intervention.

Do not simply restart the entire planner every time.

The UI must display:

- original plan
- disturbance
- reactive intervention
- repaired action sequence
- final state

Also provide the required CLI-compatible behavior:

python plan.py start.json goal.json

It should print:

- plan
- execution trace
- reactive intervention logs

If the project architecture uses another CLI entry point, provide a compatible equivalent.

---

# 9. MODULE B — REASONING UNDER UNCERTAINTY

The robot has three unreliable sensors:

1. Weight sensor
2. Vision crack detector
3. Tilt sensor

The objective is:

Determine whether a box is damaged.

Use the SAME synthetic sensor dataset across all reasoning methods.

Create at least 10 test cases.

Each test case should contain sensor evidence and, where useful, a known synthetic ground-truth label for evaluation.

---

# 10. MODULE B1 — NONMONOTONIC REASONING

Implement a simple Closed World / default-logic style system.

Default:

"Boxes are normally undamaged."

Example:

If no evidence of damage exists:
→ Not Damaged

Then add:

TiltSensorTriggered = True

The previous conclusion should be retracted or defeated.

Demonstrate explicitly:

Before new evidence:
Not Damaged

After new evidence:
Damaged / Damage Suspected

Also provide a monotonic/classical comparison demonstrating why the behavior differs.

The UI must show:

- facts
- default assumptions
- new fact
- old conclusion
- revised conclusion
- explanation

---

# 11. MODULE B2 — BAYESIAN REASONING

Implement Bayes' theorem correctly.

For each test case calculate:

P(Damaged | Evidence)

Use:

P(D|E) =
P(E|D) P(D)
----------------
P(E)

For multiple independent sensors, clearly document the conditional-independence assumption.

Use at least 5 test cases, preferably the full 10-case dataset.

Display:

- prior probability
- likelihood
- evidence probability
- posterior probability
- verdict

Do not hard-code posterior results.

Calculate them from the inputs.

---

# 12. MODULE B3 — CERTAINTY FACTORS

Implement MYCIN-style Certainty Factors.

Support:

- parallel combination
- serial combination

Use the same three sensor inputs.

Calculate the final confidence.

Compare:

CF score

against

Bayesian posterior

Explain the difference mathematically and conceptually.

Do not simply convert Bayesian probabilities into CF values.

---

# 13. MODULE B4 — BAYESIAN NETWORK

Build a small Bayesian Network with approximately 4–5 nodes.

Include concepts such as:

SensorNoise
WeightReading
CrackVisible
Tilt
Damaged

Use pgmpy or another appropriate library.

Define meaningful conditional probability tables.

Run exact inference for multiple evidence combinations.

The UI must show:

- network structure
- selected evidence
- posterior P(Damaged)
- inference result

If the chosen library version has API differences, write compatible code rather than assuming one exact API.

---

# 14. MODULE B5 — DEMPSTER-SHAFER THEORY

Implement Dempster-Shafer reasoning.

Represent each sensor using basic probability assignments over:

{Damaged, NotDamaged, Uncertain}

Implement Dempster's rule of combination.

Calculate:

- belief
- plausibility
- uncertainty interval
- conflict where applicable

The UI should show the resulting belief interval.

Clearly explain:

Bel(Damaged)

and

Pl(Damaged)

---

# 15. MODULE B6 — FUZZY LOGIC

Implement fuzzy reasoning using scikit-fuzzy.

Inputs:

weight_deviation

crack_severity

Define fuzzy sets:

weight_deviation:
- low
- medium
- high

crack_severity:
- none
- minor
- major

Create at least 4–5 rules.

Example conceptual rules:

IF weight deviation is high
AND crack severity is major
THEN damage is high.

Include additional meaningful rules covering other combinations.

Defuzzify into:

damage_score

Show:

- membership functions
- activated rules
- aggregated output
- final score

---

# 16. MODULE B7 — UNIFIED COMPARISON

Create one comparison table using the same 10 sensor cases.

Columns:

Case
Sensor Evidence
Ground Truth
Nonmonotonic Verdict
Bayes Posterior
Certainty Factor
BN Posterior
DS Belief/Plausibility
Fuzzy Score

Identify at least two cases where methods disagree.

For each disagreement add a concise technical explanation in code comments and/or UI.

Do not manufacture disagreements.

Use actual calculated outputs.

---

# 17. MODULE C — GAME PLAYING: DOCK CONTENTION

Create a small adversarial game where two robots compete for the last charging dock.

The game must have a non-trivial branching factor >= 3.

Use either:

- 4x4 pursuit/blocking grid

or

- Nim-style resource game

Prefer the 4x4 grid if it produces a clearer Streamlit visualization.

Two players:

Robot A
Robot B

Implement:

1. Plain MiniMax
2. Alpha-Beta pruning
3. Iterative Deepening
4. Move ordering heuristic

---

# 18. MODULE C1 — MINIMAX

Implement genuine recursive MiniMax.

Track:

- nodes visited
- depth
- selected action
- execution time

Do not use an external game AI library to replace the implementation.

---

# 19. MODULE C2 — ALPHA-BETA

Implement Alpha-Beta pruning on the SAME game tree.

Track:

- nodes visited
- pruned branches
- depth
- execution time

Prove that pruning occurs.

Do not fake node counts.

---

# 20. MODULE C3 — ITERATIVE DEEPENING

Implement:

depth = 1
depth = 2
depth = 3
...

Support at least depth 2–6.

Add a move-ordering heuristic.

Measure:

- decision time
- nodes explored
- selected move

Create a matplotlib chart:

X-axis:
Search Depth

Y-axis:
Nodes Explored

Lines:

MiniMax
Alpha-Beta
Alpha-Beta + IDS

The chart must use actual measured values.

---

# 21. MODULE C4 — PLAYABLE GAME

Provide CLI support similar to:

python dock_game.py --depth 5

Support:

- AI vs random
- AI vs AI

Also create a Streamlit interactive version.

The UI should visualize:

- grid
- Robot A
- Robot B
- dock
- legal moves
- selected move
- search statistics

---

# 22. MODULE D — CONNECTIONIST MODELS

Implement two neural/connectionist approaches:

1. Hopfield Network
2. RNN

---

# 23. MODULE D1 — HOPFIELD NETWORK FROM SCRATCH

Implement Hopfield Network WITHOUT a Hopfield library.

Use NumPy.

Store 4–6 binary patterns.

Represent normal box-label scan patterns as:

8 × 8 = 64-bit patterns

Convert to:

-1 / +1

Implement:

- weight matrix creation
- Hebbian learning
- energy function
- asynchronous or synchronous updates
- convergence detection

Do not use a library implementation.

---

# 24. MODULE D2 — HOPFIELD ASSOCIATIVE RECALL

Take a stored pattern.

Corrupt approximately 10–15% of its bits.

Run the Hopfield network.

Show:

Original pattern
Corrupted pattern
Recovered pattern

Calculate:

- corrupted bit count
- final difference
- recovery accuracy
- number of iterations
- energy over iterations

The Streamlit UI should visualize all three 8x8 patterns.

---

# 25. MODULE D3 — RNN ANOMALY DETECTION

Create a small sequence-classification problem.

Input:

last 10 sensor readings

Output:

whether an anomaly is imminent.

Use:

- PyTorch OR Keras/TensorFlow

Use either:

- vanilla RNN
- LSTM

Create synthetic training data if no real dataset exists.

Split into:

training
validation
test

Train the model.

Report:

- train loss
- validation loss
- test accuracy
- confusion matrix
- sample predictions

Do not display fake accuracy.

Train the actual model.

Set deterministic/random seeds where practical.

---

# 26. MODULE D4 — HOPFIELD VS RNN COMPARISON

Include a code-comment comparison table explaining:

What Hopfield can do
What Hopfield cannot do
What RNN can do
Why temporal sequence information matters

Keep the comparison practical and connected to the warehouse robot scenario.

---

# 27. MODULE E — EXPERT SYSTEM

Build a rule-based maintenance expert system.

Possible diagnoses include:

- wheel slipping
- sensor drift
- battery fault
- motor fault
- communication fault
- charging fault
- navigation fault

Create approximately 15–20 meaningful rules.

Use:

- hand-written forward-chaining engine

OR

- Experta/CLIPS

Prefer a transparent hand-rolled engine if external package compatibility becomes problematic.

---

# 28. EXPERT SYSTEM EXPLANATION FACILITY

The system must NOT only output:

Diagnosis: Battery Fault

It must also explain:

Facts observed
↓
Rule 1 fired because ...
↓
Rule 7 fired because ...
↓
Rule 12 fired because ...
↓
Final diagnosis

Every conclusion must have a rule trace.

Example:

Symptoms:
low_voltage = true
battery_temperature_high = true

Rule:
IF low_voltage AND battery_temperature_high
THEN battery_fault

Trace:

Rule R08 fired:
low_voltage=True
battery_temperature_high=True

Conclusion:
Battery Fault

---

# 29. KNOWLEDGE ACQUISITION

Provide a simple Streamlit form allowing a technician to add a rule WITHOUT modifying Python code.

Store rules in:

rules.json

A rule should contain fields such as:

- rule_id
- conditions
- diagnosis
- explanation
- priority

After saving:

- validate rule
- write JSON
- reload rules
- make rule immediately usable

Also provide a CLI-compatible expert advisor:

python expert_advisor.py ...

It should accept symptom flags and print:

Diagnosis
Why trace

---

# 30. INTEGRATION — THE MOST IMPORTANT PART

Create one integrated control loop.

The flow must be:

Sensor readings
↓
Module B — uncertainty reasoning
↓
If damage suspected
↓
Module E — expert diagnosis
↓
Explanation printed
↓
Module A — stacking/planning task
↓
If disturbance occurs
↓
Reactive planning layer
↓
Module C — dock contention side scenario
↓
Module D — anomaly detection from reading stream

This is the core "real-world" integration requirement.

---

# 31. SIMULATED SHIFT

Create a simulated warehouse shift log.

Generate approximately:

50–100 synthetic events.

Events may include:

- box scanned
- box moved
- weight sensor reading
- crack detected
- tilt triggered
- robot movement
- charging request
- dock contention
- wheel slip
- battery warning
- sensor anomaly
- box damage
- disturbance

Each event should have:

timestamp
event_type
robot_id
sensor data
optional box ID

Process the events sequentially.

---

# 32. MAIN CONTROL LOOP

Create:

main.py

It must execute the integrated simulation.

For each event:

1. Read event.
2. Update robot state.
3. Run uncertainty reasoning when relevant.
4. Detect potential damage.
5. Invoke expert system when necessary.
6. Run anomaly detection when enough sequential data exists.
7. Run planning when a task is created.
8. Trigger reactive planning when disturbance occurs.
9. Simulate dock contention when relevant.
10. Log decisions and explanations.

Produce a final shift summary.

---

# 33. STREAMLIT APPLICATION

The Streamlit application is the primary frontend.

Create a professional dashboard.

Suggested navigation:

## Dashboard

Show:

- system status
- current robot state
- current task
- current plan
- anomaly status
- damage confidence
- maintenance diagnosis
- dock status

## Planning

Tabs:

- Goal Stack
- Nonlinear Planning
- Hierarchical Planning
- Reactive Planning

Allow the user to enter or select:

Start State
Goal State

Then run the planner.

Show action traces visually.

---

## Uncertainty

Tabs:

- Nonmonotonic
- Bayes
- Certainty Factors
- Bayesian Network
- Dempster-Shafer
- Fuzzy Logic
- Comparison

Provide a sensor-input form.

Run all methods on the same evidence.

Display comparison table.

---

## Dock Game

Show:

- grid
- robots
- dock
- algorithm selector
- depth selector
- node statistics
- pruning statistics
- move history

Algorithms:

MiniMax
Alpha-Beta
Alpha-Beta + IDS

---

## Connectionist AI

Tabs:

Hopfield
RNN
Comparison

Hopfield:

- original
- corrupted
- recovered
- energy curve

RNN:

- training metrics
- test accuracy
- confusion matrix
- predictions

---

## Maintenance Expert

Provide:

- symptom checkboxes
- diagnosis
- fired rules
- explanation trace
- add-new-rule form
- rule viewer

---

## Integrated Simulation

Allow:

"Run Simulated Shift"

Display:

- event timeline
- decisions
- damage reasoning
- expert diagnosis
- anomaly detections
- planning actions
- reactive interventions
- dock events

Use Streamlit tables, metrics, expanders, charts, and status indicators.

---

# 34. DATA MANAGEMENT

Do not scatter hard-coded data throughout Python files.

Create reusable:

- dataclasses
- configuration
- JSON/CSV sample data
- helper functions

Keep synthetic datasets reproducible using a random seed.

Provide a "Generate New Synthetic Dataset" button where appropriate.

---

# 35. ERROR HANDLING

The application must not crash because of:

- missing optional data
- invalid user input
- empty evidence
- impossible planning goal
- invalid rule
- unsupported search depth
- model not trained yet
- insufficient sequence length

Show user-friendly Streamlit error/warning messages.

Use Python logging for technical diagnostics.

---

# 36. TESTING

Write automated tests for every major module.

At minimum test:

### Planning

- simple stack
- unstack
- arbitrary goal
- impossible goal
- reactive disturbance

### Uncertainty

- Bayes calculation
- CF combination
- DS combination
- fuzzy inference
- nonmonotonic retraction
- BN inference

### Game

- legal moves
- terminal states
- MiniMax
- Alpha-Beta
- pruning
- IDS

### Hopfield

- pattern storage
- corruption
- convergence
- recovery

### RNN

- dataset shape
- training
- prediction
- output shape

### Expert system

- rule firing
- diagnosis
- explanation trace
- rule loading

### Integration

- event processing
- module communication
- shift simulation

Run:

pytest

and fix all failures.

---

# 37. CODE QUALITY

Follow professional Python standards.

Use:

- type hints
- docstrings
- dataclasses where appropriate
- meaningful names
- small functions
- separation of concerns
- reusable classes
- error handling
- logging

Do not create one giant app.py file containing all algorithms.

Do not duplicate algorithms inside Streamlit UI code.

UI should call backend modules.

---

# 38. REPRODUCIBILITY

Set random seeds where appropriate.

The project should produce reproducible demonstrations.

Use a central configuration such as:

RANDOM_SEED = 42

Allow advanced users to change the seed.

---

# 39. PERFORMANCE

Avoid unnecessary retraining or recomputation on every Streamlit interaction.

Use Streamlit caching appropriately:

st.cache_data

st.cache_resource

For example:

- cache trained RNN
- cache generated datasets
- cache expensive BN construction
- cache reusable planning examples

But ensure the user can explicitly retrain/regenerate when required.

---

# 40. VISUALIZATION

Use matplotlib for required charts.

Create clear charts for:

1. MiniMax vs Alpha-Beta vs IDS node counts
2. Hopfield energy over iterations
3. RNN training/validation loss
4. RNN accuracy if applicable
5. Optional uncertainty-method comparison

Do not fake visualization data.

Charts must be generated from actual algorithm outputs.

---

# 41. README

Create a professional README.md.

It must include:

Project overview

Architecture

Installation

Python version

Dependencies

How to run Streamlit

How to run CLI modules

How to run tests

Module A explanation

Module B explanation

Module C explanation

Module D explanation

Module E explanation

Integration explanation

Example commands

Deployment instructions

Troubleshooting

Limitations

The original specification requires a one-paragraph explanation per module with a maximum of five sentences each. Keep those module explanations concise.

---

# 42. CLI REQUIREMENTS

Provide CLI entry points equivalent to:

python plan.py start.json goal.json

python dock_game.py --depth 5

python expert_advisor.py ...

If files are organized into module directories, create thin root-level wrappers if necessary so these commands remain easy to run.

---

# 43. DEPLOYMENT

The final project must be easy to deploy.

Local:

pip install -r requirements.txt

streamlit run app.py

Cloud:

Explain exactly how to deploy using Streamlit Community Cloud.

Make sure:

- no absolute Windows paths
- no hard-coded local directories
- no API keys required
- no unavailable files required
- no GPU requirement
- CPU execution works
- model training remains reasonably lightweight

If PyTorch/TensorFlow creates deployment-size problems, choose the most practical supported framework and document it.

---

# 44. NO FAKE IMPLEMENTATION

This is extremely important.

Do NOT do any of the following:

- fake algorithm outputs
- hard-code expected answers
- display random node counts
- display fake ML accuracy
- pretend a model is trained
- replace MiniMax with random choice
- replace Bayesian inference with thresholds
- replace Dempster-Shafer with an arbitrary score
- replace fuzzy logic with if/else logic
- replace Hopfield with nearest-neighbor lookup
- replace RNN with a manually calculated heuristic
- claim nonlinear planning without implementing constraints
- claim reactive planning while restarting from scratch
- create UI buttons that don't execute real backend functionality

Every displayed result must come from an actual implementation.

---

# 45. DOCUMENTATION INSIDE THE CODE

Every major algorithm should have comments explaining:

- what it does
- inputs
- outputs
- important assumptions
- mathematical formula where relevant
- why the implementation is correct

Keep comments useful rather than excessive.

---

# 46. USER EXPERIENCE

The Streamlit UI should be understandable to someone evaluating the project.

Every module should have:

1. Short description
2. Input controls
3. Run button
4. Results
5. Explanation
6. Technical details
7. Visualization where useful

Use:

- st.metric
- st.dataframe
- st.expander
- st.tabs
- st.status
- st.progress
- matplotlib
- diagrams/tables where useful

Do not overcrowd the UI.

---

# 47. IMPORTANT MATHEMATICAL CORRECTNESS

Verify formulas and algorithm implementations carefully.

Especially verify:

- Bayes theorem
- Bayesian Network inference
- Certainty Factor parallel combination
- Certainty Factor serial combination
- Dempster-Shafer mass combination
- fuzzy membership functions
- fuzzy rule aggregation
- Hopfield energy
- Hopfield weight matrix
- MiniMax recursion
- Alpha-Beta pruning
- iterative deepening
- planning preconditions/effects

Add unit tests for calculations.

---

# 48. ACCEPTANCE CRITERIA

The project is NOT complete until all of the following are true:

[ ] Project starts successfully.

[ ] Streamlit application opens.

[ ] Dashboard works.

[ ] Module A Goal Stack Planner works.

[ ] Module A nonlinear planner works.

[ ] Module A hierarchical planning works.

[ ] Module A reactive layer works.

[ ] Module B nonmonotonic reasoning works.

[ ] Module B Bayesian reasoning works.

[ ] Module B Certainty Factors works.

[ ] Module B Bayesian Network works.

[ ] Module B Dempster-Shafer works.

[ ] Module B Fuzzy Logic works.

[ ] Ten common sensor cases are evaluated.

[ ] Method comparison table works.

[ ] At least two genuine disagreement cases can be demonstrated.

[ ] Module C MiniMax works.

[ ] Module C Alpha-Beta works.

[ ] Alpha-Beta actually prunes nodes.

[ ] Iterative Deepening works.

[ ] Move ordering works.

[ ] Depth 2–6 comparison chart works.

[ ] Dock game is playable.

[ ] Module D Hopfield is implemented from scratch.

[ ] 4–6 patterns are stored.

[ ] 10–15% corruption is demonstrated.

[ ] Pattern recovery works.

[ ] Hopfield energy/convergence is shown.

[ ] Module D RNN actually trains.

[ ] RNN held-out test accuracy is calculated.

[ ] Module E contains approximately 15–20 rules.

[ ] Expert system performs forward chaining.

[ ] Rule trace is displayed.

[ ] Knowledge acquisition interface works.

[ ] Rules can be added without changing Python code.

[ ] Integrated control loop works.

[ ] 50–100 synthetic shift events can be processed.

[ ] Module interactions are visible.

[ ] Tests pass.

[ ] requirements.txt works.

[ ] README is complete.

[ ] Deployment instructions work.

---

# 49. DEVELOPMENT PROCESS

Follow this exact development order:

PHASE 1:
Audit existing repository.

PHASE 2:
Create/fix project architecture.

PHASE 3:
Fix Module A.

PHASE 4:
Fix Module B.

PHASE 5:
Fix Module C.

PHASE 6:
Fix Module D.

PHASE 7:
Fix Module E.

PHASE 8:
Build integration/control loop.

PHASE 9:
Build Streamlit frontend.

PHASE 10:
Create CLI wrappers.

PHASE 11:
Create tests.

PHASE 12:
Run complete test suite.

PHASE 13:
Run Streamlit application.

PHASE 14:
Perform end-to-end smoke test.

PHASE 15:
Fix all errors.

PHASE 16:
Prepare deployment files.

PHASE 17:
Prepare final README.

---

# 50. FINAL REPORT TO ME

After implementation, give me a concise final engineering report containing:

## A. What you found

List the major problems in the original project.

## B. What you changed

List every major modification.

## C. Module status

For each:

Module A
Module B
Module C
Module D
Module E
Integration

Report:

Implemented
Tested
Known limitations

## D. Files created/modified

Give a complete file tree.

## E. How to run

Give exact commands.

Example:

pip install -r requirements.txt

streamlit run app.py

pytest

## F. Deployment

Give exact Streamlit deployment steps.

## G. Verification

Report:

- tests passed
- Streamlit startup verified
- major algorithms verified
- integration verified

Do not claim something was tested if it was not actually tested.

---

# 51. MOST IMPORTANT INSTRUCTION

Treat the original PDF specification as the authoritative requirements document.

Do not silently omit difficult requirements.

Do not simplify away the academic concepts.

Do not create a presentation-only project.

Build a genuine working implementation.

If an existing implementation is partially correct, improve it instead of unnecessarily rewriting everything.

If a dependency is incompatible with the deployment environment, replace it only after preserving the required functionality and document the replacement.

If something from the specification cannot technically be implemented exactly because of a dependency/version limitation, explicitly explain the limitation and implement the closest technically correct solution.

The final result should be:

**A complete, modular, tested, explainable, Streamlit-based Python AI/ML warehouse robot brain that can be run locally and deployed easily.**

Start by auditing the existing project before making changes.

Do not stop after the audit.

Proceed through implementation, testing, integration, UI, and deployment preparation until the acceptance criteria are satisfied.