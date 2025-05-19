import networkx as nx
import matplotlib.pyplot as plt
import random
import json

# Parameters
N = 5000  # Number of nodes (city population)
k = 10  # Average degree
p = 0.1  # Rewiring probability
beta = 0.03  # Transmission probability
recovery_days = 14  # Days to recover
initial_infected = 50  # Initial number of infected nodes
days = 100  # Simulation duration

# Generate Watts-Strogatz small-world network
G = nx.watts_strogatz_graph(N, k, p)

# Initialize node states
node_states = {node: 'S' for node in G.nodes()}  # S: Susceptible, I: Infected, R: Recovered
days_infected = {node: 0 for node in G.nodes()}

# Infect initial nodes
initial_infected_nodes = random.sample(list(G.nodes()), initial_infected)
for node in initial_infected_nodes:
    node_states[node] = 'I'

# Simulation
simulation_data = []  # To store data for real-time visualization
daily_network_states = []  # To store node states for each day

susceptible_count = []
infected_count = []
recovered_count = []

for day in range(days):
    new_infections = []
    new_recoveries = []

    for node in G.nodes():
        if node_states[node] == 'I':
            # Attempt to infect neighbors
            for neighbor in G.neighbors(node):
                if node_states[neighbor] == 'S' and random.random() < beta:
                    new_infections.append(neighbor)
            # Increment days infected
            days_infected[node] += 1
            if days_infected[node] >= recovery_days:
                new_recoveries.append(node)

    # Update states
    for node in new_infections:
        node_states[node] = 'I'
    for node in new_recoveries:
        node_states[node] = 'R'

    # Track counts
    susceptible_count.append(sum(1 for state in node_states.values() if state == 'S'))
    infected_count.append(sum(1 for state in node_states.values() if state == 'I'))
    recovered_count.append(sum(1 for state in node_states.values() if state == 'R'))

    # Store data for visualization
    simulation_data.append({
        "day": day,
        "susceptible": susceptible_count[-1],
        "infected": infected_count[-1],
        "recovered": recovered_count[-1],
    })

    # Store daily network state
    daily_network_states.append({
        "day": day,
        "node_states": {node: node_states[node] for node in G.nodes()}
    })

# Save simulation data to JSON
with open("simulation_data.json", "w") as f:
    json.dump(simulation_data, f)

# Save daily network states to JSON
with open("daily_network_states.json", "w") as f:
    json.dump(daily_network_states, f)

# Visualization of the network
color_map = {'S': 'green', 'I': 'red', 'R': 'blue'}
node_colors = [color_map[node_states[node]] for node in G.nodes()]
pos = nx.spring_layout(G)  # Force-directed graph layout
plt.figure(figsize=(12, 8))
nx.draw(G, pos, node_color=node_colors, with_labels=False, node_size=10)
plt.title('Social Network Visualization with Infection States')
plt.show()

# Plot infection curve
plt.figure(figsize=(10, 6))
plt.plot(susceptible_count, label='Susceptible', color='green')
plt.plot(infected_count, label='Infected', color='red')
plt.plot(recovered_count, label='Recovered', color='blue')
plt.xlabel('Days')
plt.ylabel('Number of Individuals')
plt.title('SIR Model Simulation')
plt.legend()
plt.show()
