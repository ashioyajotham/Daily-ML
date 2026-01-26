def maximum_saving(input_network: str) -> int:
    """
    Calculates the maximum saving achievable by removing redundant edges
    while maintaining network connectivity (finding the Minimum Spanning Tree).
    """
    
    # --- Helper: Union-Find Data Structure for Kruskal's Algorithm ---
    class UnionFind:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, u):
            if self.parent[u] != u:
                self.parent[u] = self.find(self.parent[u])  # Path compression
            return self.parent[u]

        def union(self, u, v):
            root_u = self.find(u)
            root_v = self.find(v)

            if root_u != root_v:
                # Union by rank
                if self.rank[root_u] > self.rank[root_v]:
                    self.parent[root_v] = root_u
                elif self.rank[root_u] < self.rank[root_v]:
                    self.parent[root_u] = root_v
                else:
                    self.parent[root_v] = root_u
                    self.rank[root_u] += 1
                return True
            return False

    # --- 1. Parse the Input ---
    # Split the input string into rows and clean up whitespace
    rows = [line.strip() for line in input_network.strip().split('\n')]
    
    edges = []
    total_network_cost = 0
    num_nodes = len(rows)

    # Iterate through the matrix to extract edges
    # We only look at j > i to avoid duplicates in an undirected graph
    for i in range(num_nodes):
        # Split the CSV row
        cols = rows[i].split(',')
        for j in range(i + 1, num_nodes):
            val = cols[j].strip()
            if val != '-':
                weight = int(val)
                edges.append((i, j, weight))
                total_network_cost += weight

    # --- 2. Kruskal's Algorithm to find MST ---
    # Sort edges by weight (ascending)
    edges.sort(key=lambda x: x[2])

    uf = UnionFind(num_nodes)
    mst_cost = 0
    edges_count = 0

    for u, v, weight in edges:
        # If adding this edge doesn't form a cycle
        if uf.union(u, v):
            mst_cost += weight
            edges_count += 1
            
            # Optimization: Stop if we have selected V-1 edges (MST is complete)
            if edges_count == num_nodes - 1:
                break

    # --- 3. Calculate Savings ---
    return total_network_cost - mst_cost

# Example usage based on the problem description
if __name__ == "__main__":
    input_network = '''-,14,10,19,-,-,-
14,-,-,15,18,-,-
10,-,-,26,-,29,-
19,15,26,-,16,17,21
-,18,-,16,-,-,9
-,-,29,17,-,-,25
-,-,-,21,9,25,-'''

    max_saving = maximum_saving(input_network)
    print(max_saving)