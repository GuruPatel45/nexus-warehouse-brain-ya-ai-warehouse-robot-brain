# Uncertainty-Aware Warehouse Robot Brain

This project implements a complete, modular, and testable warehouse robot intelligence system that handles planning, reasoning under uncertainty, adversarial games, connectionist models, and an expert system, all coordinated by a central integration control loop.

## Architecture
- **app.py**: The main entry point for the Streamlit multipage application.
- **modules/**: Contains the 5 intelligence modules and the integration logic.
  - `planning/`: Block world planning algorithms (Goal Stack, POP, Hierarchical, Reactive).
  - `uncertainty/`: Probability and reasoning formalisms (Bayes, CF, BN, Dempster-Shafer, Fuzzy, Nonmonotonic).
  - `game/`: Adversarial search (MiniMax, AlphaBeta, IDS) for dock contention.
  - `connectionist/`: Hopfield associative memory and RNN anomaly detection.
  - `expert_system/`: Forward-chaining rule engine for diagnostics.
  - `integration/`: The central control loop and shift log generation.
- **ui/**: The Streamlit UI pages corresponding to each module.
- **tests/**: Automated unit tests inside each module directory.

## Installation & Setup

Requirements:
- Python 3.10+

```bash
# Clone the repository and cd into it
# Install the dependencies
pip install -r requirements.txt
```

## Running the Streamlit Application
Launch the graphical interface which provides dashboards for all modules:
```bash
streamlit run app.py
```

## Running CLI Wrappers
We provide thin root-level wrappers for CLI access:

```bash
# Run Planning 
python plan.py data/start.json data/goal.json

# Run Dock Contention Game
python dock_game.py --depth 5 --opponent random

# Run Expert System Knowledge Acquisition / Advisor
python expert_advisor.py
```

## Running Tests
Ensure mathematical correctness of all algorithms:
```bash
export PYTHONPATH="."
pytest modules/
```

## Deployment to Streamlit Community Cloud
This application is fully compatible with [Streamlit Community Cloud](https://streamlit.io/cloud).

1. Push this repository to a public or private GitHub repository.
2. Log in to Streamlit Community Cloud.
3. Click **New app** and select your GitHub repository.
4. Set the **Main file path** to `app.py`.
5. Click **Deploy!**

The cloud environment will automatically install dependencies listed in `requirements.txt`. There are no API keys, local hardcoded paths, or GPU dependencies required.

## Module Explanations

### Module A (Planning)
Implements an extended Goal Stack Planner, a Nonlinear (Partial-Order) Planner, and Hierarchical decomposition to stack pallets. It includes a reactive layer capable of handling disturbances (e.g., knocked over blocks) by adjusting the plan on the fly. 

### Module B (Uncertainty)
Evaluates noisy sensor telemetry using six different formalisms: Nonmonotonic logic, Bayes' Theorem, Certainty Factors, Bayesian Networks, Dempster-Shafer theory, and Fuzzy Logic. It provides a comparative analysis to demonstrate edge cases where the methods disagree.

### Module C (Game Playing)
Simulates a multi-agent dock contention scenario using adversarial search. It demonstrates plain MiniMax, Alpha-Beta pruning, and Iterative Deepening Search, including benchmarking graphs that prove Alpha-Beta correctly prunes branches.

### Module D (Connectionist Models)
Implements a Hopfield Network from scratch in NumPy to provide content-addressable memory for recalling corrupted visual symbols. It also features a PyTorch RNN trained to detect temporal anomalies in sequence data.

### Module E (Expert System)
Provides a pure-Python forward-chaining rule engine to diagnose robot faults. It generates an explicit trace explaining why each rule fired and includes a knowledge acquisition tool to add rules without modifying code.

### Integration
Generates synthetic shift logs with up to 100 random events and processes them sequentially in a central control loop. It links all modules together, chaining uncertainty evaluations into expert diagnostics and triggering reactive planning during disturbances.
