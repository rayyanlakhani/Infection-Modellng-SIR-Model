import networkx as nx
import matplotlib.pyplot as plt
import random
import json

# Parameters
N = 500  # Number of nodes (city population)
k = 4  # Average degree
p = 0.1  # Rewiring probability
beta = 0.05  # Transmission probability
recovery_days = 14  # Days to recover
initial_infected = 50  # Initial number of infected nodes
days = 50  # Simulation duration
#death_rate = 0.05  # Probability of death for infected individuals

# Generate Watts-Strogatz small-world network
G = nx.watts_strogatz_graph(N, k, p)

# Initialize node states
node_states = {node: 'S' for node in G.nodes()}  # S: Susceptible, I: Infected, R: Recovered, D: Dead
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
    # new_deaths = []

    for node in G.nodes():
        if node_states[node] == 'I':
            # Attempt to infect neighbors
            for neighbor in G.neighbors(node):
                if node_states[neighbor] == 'S' and random.random() < beta:
                    new_infections.append(neighbor)
            # Increment days infected
            days_infected[node] += 1
            # Check for death
            # if random.random() < death_rate:
            #     new_deaths.append(node)
            if days_infected[node] >= recovery_days:
                new_recoveries.append(node)

    # Update states
    for node in new_infections:
        node_states[node] = 'I'
    for node in new_recoveries:
        node_states[node] = 'R'
    # for node in new_deaths:
    #     node_states[node] = 'D'

    # Track counts
    susceptible_count.append(sum(1 for state in node_states.values() if state == 'S'))
    infected_count.append(sum(1 for state in node_states.values() if state == 'I'))
    recovered_count.append(sum(1 for state in node_states.values() if state == 'R'))
    dead_count = sum(1 for state in node_states.values() if state == 'D')

    # Store data for visualization
    simulation_data.append({
        "day": day,
        "susceptible": susceptible_count[-1],
        "infected": infected_count[-1],
        "recovered": recovered_count[-1],
        "dead": dead_count,
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

# Visualization of the network (final state)
color_map = {'S': 'green', 'I': 'red', 'R': 'blue', 'D': 'black'}
node_colors = [color_map[node_states[node]] for node in G.nodes()]
pos = nx.spring_layout(G, seed=42)  # Force-directed graph layout with fixed seed for consistency
plt.figure(figsize=(14, 10))
nx.draw(
    G,
    pos,
    node_color=node_colors,
    with_labels=False,
    node_size=20,
    edge_color="gray",
    alpha=0.7
)
plt.title('Social Network Visualization with Infection States (Final Day)', fontsize=16)
plt.show()

# Visualization of the network (initial state)
initial_node_colors = ['red' if node in initial_infected_nodes else 'green' for node in G.nodes()]
plt.figure(figsize=(14, 10))
nx.draw(
    G,
    pos,
    node_color=initial_node_colors,
    with_labels=False,
    node_size=20,
    edge_color="gray",
    alpha=0.7
)
plt.title('Social Network Visualization with Initial Infection', fontsize=16)
plt.show()

# Plot infection curve
plt.figure(figsize=(10, 6))
plt.plot(susceptible_count, label='Susceptible', color='green')
plt.plot(infected_count, label='Infected', color='red')
plt.plot(recovered_count, label='Recovered', color='blue')
plt.plot([data["dead"] for data in simulation_data], label='Dead', color='black')
plt.xlabel('Days')
plt.ylabel('Number of Individuals')
plt.title('SIR Model Simulation with Deaths')
plt.legend()
plt.show()

def visualize_force_directed_graph(G, node_states, title):
    """
    Visualize the network using a force-directed graph layout.
    """
    color_map = {'S': 'green', 'I': 'red', 'R': 'blue', 'D': 'black'}
    node_colors = [color_map[node_states[node]] for node in G.nodes()]
    pos = nx.spring_layout(G, seed=42)  # Force-directed layout with fixed seed for consistency

    plt.figure(figsize=(14, 10))
    nx.draw(
        G,
        pos,
        node_color=node_colors,
        with_labels=False,
        node_size=50,
        edge_color="gray",
        alpha=0.7
    )
    plt.title(title, fontsize=16)
    plt.show()

# Visualization of the network (force-directed graph for the final state)
visualize_force_directed_graph(G, node_states, 'Force-Directed Graph: Final Infection States')

# Visualization of the network (force-directed graph for the initial state)
initial_node_states = {node: 'I' if node in initial_infected_nodes else 'S' for node in G.nodes()}
visualize_force_directed_graph(G, initial_node_states, 'Force-Directed Graph: Initial Infection States')
