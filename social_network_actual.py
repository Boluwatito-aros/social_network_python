from collections import deque


class Graph:
    def __init__(self):
        self.a_graph = {}

    def add_new(self, name, age, interests):
        self.a_graph[name] = {"age": age, "interests": interests, "relations": {}}
        return self.a_graph

    def remove(self, name):
        self.a_graph.pop(name)
        return self.a_graph

    def add_rel(self, node1, node2, weight):
        self.a_graph[node1]["relations"][node2] = weight
        return self.a_graph

    def rem_rel(self, node1, node2):
        self.a_graph[node1]["relations"].pop(node2, None)
        return self.a_graph

    def find_friends(self, node1):
        return self.a_graph[node1]["relations"] if node1 in self.a_graph else []

    def find_mutuals(self, node1, node2):
        node_rel1 = list(self.a_graph[node1]["relations"].keys())
        node_rel2 = list(self.a_graph[node2]["relations"].keys())  # Fix: was node1 twice
        mutuals = []
        for fr in node_rel1:
            if fr in node_rel2:
                mutuals.append(fr)
        return mutuals

    def suggest_friends(self, node1):
        """Suggest friends based on second-degree relationships (friends of friends)."""
        direct = set(self.a_graph[node1]["relations"].keys())
        suggestions = set()
        for friend in direct:
            for second in self.a_graph[friend]["relations"].keys():
                if second != node1 and second not in direct:
                    suggestions.add(second)
        return list(suggestions)

    def sh_path(self, node1, node2):
        q = deque()  # Use deque for efficient BFS
        q.append([node1])
        while q:
            current = q.popleft()  # Fix: was pop(0), deque.popleft() is O(1)
            node = current[-1]
            if node == node2:
                edges = len(current) - 1
                return current, edges
            for n in self.a_graph[node]["relations"]:
                if n not in current:
                    new_path = current + [n]
                    q.append(new_path)
        return None, -1  # No path found

    def degrees(self, node1, node2):
        """Return degrees of separation between two users."""
        path, edges = self.sh_path(node1, node2)  # Fix: was using len() on sh_path incorrectly
        return edges

    def most_conn(self):
        max_con = 0
        greatest_con = []  # Fix: use list instead of string concatenation
        for member in self.a_graph:
            connections = self.a_graph[member]["relations"]
            if len(connections) > max_con:
                greatest_con = [member]  # Fix: store name not dict value
                max_con = len(connections)
            elif len(connections) == max_con:
                greatest_con.append(member)
        return f"{greatest_con} with {max_con} connections"

    def clusters(self):
        """Find all connected clusters in the network using BFS."""
        visited = set()  # Fix: original loop had infinite loop bug
        clusts = []
        for member in self.a_graph:
            if member not in visited:
                q = deque([member])
                clust1 = []
                while q:
                    current = q.popleft()
                    if current not in visited:
                        visited.add(current)
                        clust1.append(current)
                        for n in self.a_graph[current]["relations"]:
                            if n not in visited:
                                q.append(n)
                clusts.append(clust1)
        return clusts
    

g = Graph()
g.add_new("Alice", 22, ["music", "coding"])
g.add_new("Bob", 25, ["coding", "football"])
g.add_new("Carol", 23, ["music", "art"])
g.add_new("Dave", 28, ["football", "gaming"])
g.add_new("Eve", 21, ["art", "coding"])
g.add_new("Frank", 30, ["gaming"])


g.add_rel("Alice", "Bob", 1)
g.add_rel("Bob", "Alice", 1)
g.add_rel("Alice", "Carol", 1)
g.add_rel("Carol", "Alice", 1)
g.add_rel("Bob", "Dave", 1)
g.add_rel("Dave", "Bob", 1)
g.add_rel("Carol", "Eve", 1)
g.add_rel("Eve", "Carol", 1)
g.add_rel("Dave", "Eve", 1)
g.add_rel("Eve", "Dave", 1)
g.add_rel("Dave", "Frank", 1)
g.add_rel("Frank", "Dave", 1)

print("=== find_friends ===")
print(g.find_friends("Alice"))

print("\n=== find_mutuals ===")
print(g.find_mutuals("Alice", "Bob"))

print(g.find_mutuals("Bob", "Eve"))


print("\n=== most_conn ===")
print(g.most_conn())