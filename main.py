import heapq
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import itertools

def addEdge(graph, u, v, weight):
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    if v not in graph[u]:
        graph[u][v] = weight
    if u not in graph[v]:
        graph[v][u] = weight

def calcDistance(coord_a, coord_b):
    coord_a = tuple(map(float, coord_a.split(',')))
    coord_b = tuple(map(float, coord_b.split(',')))
    return geodesic(coord_a, coord_b).km

def dijkstra(graph, start, end):
    priority_queue = []
    distances = {vertex: float('infinity') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start] = 0
    heapq.heappush(priority_queue, (0, start))

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex == end:
            break

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    path.reverse()

    return distances[end], path

def fetchCoordinatesFromCEP(cep):
    geolocator = Nominatim(user_agent="dijkstra_app")
    try:
        cep = cep.replace('-', '')
        location = geolocator.geocode(cep)
        if location:
            return f"{location.latitude},{location.longitude}"
        else:
            print(f"Erro: Não foi possível encontrar o CEP '{cep}'.")
            return None
    except Exception as e:
        print(f"Erro ao buscar o CEP '{cep}': {e}")
        return None

def plotGraph(graph, path):
    G = nx.Graph()

    for u in graph:
        for v, weight in graph[u].items():
            G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')

    weights = nx.get_edge_attributes(G, 'weight')
    edge_labels = {edge: f"{weights[edge]:.2f}" for edge in G.edges()}

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, alpha=0.7)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()

print("Bem-vindo ao sistema de cálculo de distâncias!")
num_places = int(input("Quantos locais você deseja adicionar? "))

places = []

for i in range(num_places):
    name = input(f"Digite o nome do local {i + 1}: ")
    cep = input(f"Digite o CEP do local '{name}': ")
    coordinates = fetchCoordinatesFromCEP(cep)
    if coordinates:
        places.append((name, coordinates))
    else:
        print(f"CEP '{cep}' inválido. Tente novamente.")

if len(places) < 2:
    print("É necessário adicionar pelo menos dois locais para calcular distâncias.")
    exit()

print("\nLocais adicionados:")
for place in places:
    print(place)

print("\nCalculando distâncias entre os locais...")
combinations = itertools.combinations(places, 2)
data = []
for place1, place2 in combinations:
    u, coord_u = place1
    v, coord_v = place2
    weight = calcDistance(coord_u, coord_v)
    data.append((u, v, weight))
    print(f"Distância de {u} a {v}: {weight:.2f} km")

graph = {}
for u, v, weight in data:
    addEdge(graph, u, v, weight)

start_vertex = input("\nDigite o nome do local de partida: ")
end_vertex = input("Digite o nome do local de destino: ")

if start_vertex not in graph or end_vertex not in graph:
    print(f"Erro: Os nós '{start_vertex}' ou '{end_vertex}' não estão no grafo.")
else:
    distance, path = dijkstra(graph, start_vertex, end_vertex)

    print(f"\nA menor distância de {start_vertex} a {end_vertex} é {distance:.2f} km")
    print(f"O caminho é: {' -> '.join(path)}")

    plotGraph(graph, path)
