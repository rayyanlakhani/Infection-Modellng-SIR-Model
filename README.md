# Infection-Modelling-SIR-Model

# Simulating Infectious Disease Spread in a Social Network

This project models the spread of an infectious disease (like COVID-19) through a synthetic social network of a city population using the SIR model.

## Features

1. **Synthetic Social Network Generation**:

   - Uses the Watts-Strogatz model to simulate a realistic social network with clustering and random interactions.

2. **Force-Directed Graph Visualization**:

   - Visualizes the social network with infected, susceptible, and recovered nodes color-coded.

3. **Disease Spread Simulation**:
   - Simulates the spread of infection using the SIR model with configurable parameters.

## How to Run

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the simulation:

   ```bash
   python sir_simulation.py
   ```

3. View the generated infection curve and network visualization.

4. Open `visualization.html` in a browser to view real-time simulation data.

## Parameters

- `N`: Number of nodes (city population).
- `k`: Average degree of nodes.
- `p`: Rewiring probability for the Watts-Strogatz model.
- `beta`: Infection transmission probability.
- `recovery_days`: Number of days for an infected individual to recover.
- `initial_infected`: Initial number of infected individuals.
- `days`: Duration of the simulation.

## Visualization

- **Graph**: Force-directed layout with color-coded nodes:
  - Green: Susceptible
  - Red: Infected
  - Blue: Recovered
- **Infection Curve**: Tracks the number of susceptible, infected, and recovered individuals over time.
