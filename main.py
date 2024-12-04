import heapq
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import itertools

def addEdge(graph, u, v, weight):
    if u not in graph:
        graph[u] = {}
    if v not in graph:
        graph[v] = {}
    graph[u][v] = weight
    graph[v][u] = weight

def calcDistance(coord_a, coord_b):
    distance = geodesic(coord_a, coord_b).km
    return distance

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

def fetchLocation(postcode):
    geolocator = Nominatim(user_agent="Djikstra")
    location = geolocator.geocode(postcode)
    return location

def parseCoordinates(location):
    coordinates = (location.latitude, location.longitude)
    return coordinates

def plotGraph(graph, path):

    G = nx.Graph()

    for u in graph:
        for v, weight in graph[u].items():
            G.add_edge(u, v, weight=weight)

    pos = nx.spring_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')

    edges = G.edges()
    weights = nx.get_edge_attributes(G, 'weight')
    edge_labels = {edge: f"{weights[edge]:.2f}" for edge in edges}

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()

places = [('A', '-80.713937, 57.406936'),
('B', '38.67153, 87.039646'),
('C', '2.797919, -35.300138'),
('D', '-67.529481, 39.976455'),
('E', '22.698894, 36.315485'),
]
combinations = itertools.combinations(places, 2)

data = []
for places in combinations:
    data.append( (places[0][0], places[1][0],
    calcDistance (places[0][1], places[1][1]) ) )
print(data)

graph = {}
for u, v, weight in data:
    addEdge(graph, u, v, weight)

start_vertex = 'A'
end_vertex = 'E'
distance, path = dijkstra(graph, start_vertex, end_vertex)
for u, v, weight in data:
    addEdge(graph, u, v, weight)

# Exibindo o resultado
print(f"A menor distância de {start_vertex} a {end_vertex} é {distance}")
print(f"O caminho é: {' -> '.join(path)}")

plotGraph(graph, path)
