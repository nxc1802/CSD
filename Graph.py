class Vertex:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.connected_to = {}

    def add_neighbor(self, nbr):
        distance = self.calculate_distance(self.coordinates, nbr.coordinates)
        self.connected_to[nbr] = distance

    def get_connections(self):
        return self.connected_to.keys()

    def get_coordinates(self):
        return self.coordinates

    def get_weight(self, nbr):
        return self.connected_to[nbr]

    @staticmethod
    def calculate_distance(coord1, coord2):
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2 + (coord1[2] - coord2[2]) ** 2) ** 0.5


class Graph:
    def __init__(self):
        self.vert_list = {}

    def add_vertex(self, coordinates):
        new_vertex = Vertex(coordinates)
        self.vert_list[coordinates] = new_vertex
        self._add_edges_for_new_vertex(new_vertex)
        return new_vertex

    def get_vertex(self, coordinates):
        return self.vert_list.get(coordinates)

    def _add_edges_for_new_vertex(self, new_vertex):
        new_coords = new_vertex.coordinates
        for v in self.vert_list.values():
            if v == new_vertex:
                continue
            coords = v.coordinates
            if self._are_adjacent(coords, new_coords):
                v.add_neighbor(new_vertex)
                new_vertex.add_neighbor(v)

    def _are_adjacent(self, coords1, coords2):
        diff_count = sum([abs(coords1[i] - coords2[i]) == 10 for i in range(3)])
        same_count = sum([coords1[i] == coords2[i] for i in range(3)])
        return diff_count == 1 and same_count == 2

    def dijkstra(self, start_coordinates):
        if start_coordinates not in self.vert_list:
            return None

        distances = {vertex: float('infinity') for vertex in self.vert_list}
        distances[start_coordinates] = 0
        pq = [(start_coordinates, 0)]
        mst = []
        visited = set()

        while pq:
            current_coordinates, current_distance = min(pq, key=lambda x: x[1])
            pq.remove((current_coordinates, current_distance))

            if current_coordinates in visited:
                continue

            visited.add(current_coordinates)
            current_vertex = self.get_vertex(current_coordinates)

            for neighbor in current_vertex.get_connections():
                neighbor_coordinates = neighbor.get_coordinates()
                edge_weight = current_vertex.get_weight(neighbor)
                distance = current_distance + edge_weight

                if distance < distances[neighbor_coordinates]:
                    distances[neighbor_coordinates] = distance
                    pq.append((neighbor_coordinates, distance))
                    mst.append((current_coordinates, neighbor_coordinates, edge_weight))

        total_weight = sum(weight for _, _, weight in mst)
        return mst, total_weight


# Example usage
if __name__ == '__main__':
    g = Graph()
    vertices = [
        (0, 0, 0), (0, 0, 10), (0, 0, 20), (0, 0, 30), 
        (10, 0, 0), (10, 0, 10), (10, 0, 20), (10, 0, 30), 
        (0, 10, 0), (0, 10, 10), (0, 10, 20), (0, 10, 30), 
        (10, 10, 0), (10, 10, 10), (10, 10, 20), (10, 10, 30), 
        (0, 20, 0), (0, 20, 10), (10, 20, 0), (10, 20, 10)
    ]

    for vertex in vertices:
        g.add_vertex(vertex)

    print('Minimum Spanning Tree (MST) using Dijkstra:')
    mst, total_weight = g.dijkstra(vertices[0])
    print("Edges in MST:")
    print("Tầng 1")
    for i in mst:
        if i[0][2] == 0:
            print(i[0], i[1])
    print("Tầng 2")
    for i in mst:
        if i[0][2] == 10:
            print(i[0], i[1])
    print("Tầng 3")
    for i in mst:
        if i[0][2] == 20:
            print(i[0], i[1])
    print("Tầng 4")
    for i in mst:
        if i[0][2] == 30:
            print(i[0], i[1])
    print(f"Total weight of MST: {total_weight}")
