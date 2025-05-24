import networkx as nx
import matplotlib.pyplot as plt
import random
import json


N = 500
k = 4
p = 0.1
beta = 0.05
recovery_days = 14
initial_infected = 50
days = 50  
#death_rate = 0.05  # Probability of death for infected individuals


G = nx.watts_strogatz_graph(N, k, p)


node_states = {node: 'S' for node in G.nodes()}
days_infected = {node: 0 for node in G.nodes()}


initial_infected_nodes = random.sample(list(G.nodes()), initial_infected)
for node in initial_infected_nodes:
    node_states[node] = 'I'


simulation_data = [] 
daily_network_states = []

susceptible_count = []
infected_count = []
recovered_count = []

for day in range(days):
    new_infections = []
    new_recoveries = []
    # new_deaths = []

    for node in G.nodes():
        if node_states[node] == 'I':
            
            for neighbor in G.neighbors(node):
                if node_states[neighbor] == 'S' and random.random() < beta:
                    new_infections.append(neighbor)
            
            days_infected[node] += 1
            # Check for death
            # if random.random() < death_rate:
            #     new_deaths.append(node)
            if days_infected[node] >= recovery_days:
                new_recoveries.append(node)

    
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

    
    simulation_data.append({
        "day": day,
        "susceptible": susceptible_count[-1],
        "infected": infected_count[-1],
        "recovered": recovered_count[-1],
        "dead": dead_count,
    })

    
    daily_network_states.append({
        "day": day,
        "node_states": {node: node_states[node] for node in G.nodes()}
    })


with open("simulation_data.json", "w") as f:
    json.dump(simulation_data, f)


with open("daily_network_states.json", "w") as f:
    json.dump(daily_network_states, f)


color_map = {'S': 'green', 'I': 'red', 'R': 'blue', 'D': 'black'}
node_colors = [color_map[node_states[node]] for node in G.nodes()]
pos = nx.spring_layout(G, seed=42)  
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
    pos = nx.spring_layout(G, seed=42) 

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


visualize_force_directed_graph(G, node_states, 'Force-Directed Graph: Final Infection States')


initial_node_states = {node: 'I' if node in initial_infected_nodes else 'S' for node in G.nodes()}
visualize_force_directed_graph(G, initial_node_states, 'Force-Directed Graph: Initial Infection States')
