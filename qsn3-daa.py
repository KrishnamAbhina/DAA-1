import random
import time
import heapq

# Function to obtain user-defined bases
def input_bases():
    num_bases = int(input("Enter the number of bases: "))
    bases_list = []
    for i in range(num_bases):
        x_coord = int(input(f"Enter x-coordinate for base {i+1}: "))
        y_coord = int(input(f"Enter y-coordinate for base {i+1}: "))
        bases_list.append((x_coord, y_coord))
    return bases_list

# Prim's algorithm using a simple list (array-based priority queue)
def prim_mst_array_based(bases_list):
    num_bases = len(bases_list)
    visited_bases = [False] * num_bases
    total_cost = 0
    priority_queue = [(0, 0)]  # (cost, base_index)

    while priority_queue:
        min_cost, current_base = min(priority_queue)
        priority_queue.remove((min_cost, current_base))
        if visited_bases[current_base]:
            continue
        visited_bases[current_base] = True
        total_cost += min_cost

        for other_base in range(num_bases):
            if not visited_bases[other_base]:
                edge_cost = min(
                    abs(bases_list[current_base][0] - bases_list[other_base][0]),
                    abs(bases_list[current_base][1] - bases_list[other_base][1])
                )
                priority_queue.append((edge_cost, other_base))

    return total_cost

# Prim's algorithm using a binary heap
def prim_mst_binary_heap(bases_list):
    num_bases = len(bases_list)
    visited_bases = [False] * num_bases
    total_cost = 0
    priority_queue = [(0, 0)]  # (cost, base_index)

    while priority_queue:
        min_cost, current_base = heapq.heappop(priority_queue)
        if visited_bases[current_base]:
            continue
        visited_bases[current_base] = True
        total_cost += min_cost

        for other_base in range(num_bases):
            if not visited_bases[other_base]:
                edge_cost = min(
                    abs(bases_list[current_base][0] - bases_list[other_base][0]),
                    abs(bases_list[current_base][1] - bases_list[other_base][1])
                )
                heapq.heappush(priority_queue, (edge_cost, other_base))

    return total_cost

# Node class for Fibonacci Heap
class FibonacciHeapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.degree = 0
        self.is_marked = False
        self.parent = self.child = None
        self.left = self.right = self

# Fibonacci Heap class
class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.node_count = 0

    def add_node(self, key, value):
        if self.node_count >= 1000000:  # Preventing heap overflow
            raise ValueError("Fibonacci heap size limit exceeded")
        new_node = FibonacciHeapNode(key, value)
        if not self.min_node:
            self.min_node = new_node
        else:
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.node_count += 1

    def get_min(self):
        if not self.min_node:
            return None
        min_node = self.min_node
        if min_node.child:
            children = list(self._get_children(min_node))
            for child in children:
                self._add_to_root_list(child)
                child.parent = None
        self._remove_from_root_list(min_node)
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()
        self.node_count -= 1
        return min_node.key, min_node.value

    def _add_to_root_list(self, node):
        if not self.min_node:
            self.min_node = node
        else:
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node

    def _remove_from_root_list(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def _get_children(self, node):
        children = []
        current_child = node.child
        while current_child:
            children.append(current_child)
            current_child = current_child.right
            if current_child == node.child:
                break
        return children

    def _consolidate(self):
        max_degree = int(self.node_count**0.5) + 1
        degree_table = [None] * max_degree

        for node in self._get_root_list():
            degree = node.degree
            while degree_table[degree]:
                other = degree_table[degree]
                if node.key > other.key:
                    node, other = other, node
                self._link_nodes(other, node)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = node

        self.min_node = None
        for node in degree_table:
            if node:
                if not self.min_node:
                    self.min_node = node
                else:
                    self._add_to_root_list(node)
                    if node.key < self.min_node.key:
                        self.min_node = node

    def _link_nodes(self, child, parent):
        self._remove_from_root_list(child)
        child.parent = parent
        if not parent.child:
            parent.child = child
            child.left = child.right = child
        else:
            child.left = parent.child.left
            child.right = parent.child
            parent.child.left.right = child
            parent.child.left = child
        parent.degree += 1
        child.is_marked = False

    def _get_root_list(self):
        if not self.min_node:
            return
        current = self.min_node
        while True:
            yield current
            current = current.right
            if current == self.min_node:
                break

# Prim's algorithm using Fibonacci Heap
def prim_mst_fib_heap(bases_list):
    num_bases = len(bases_list)
    visited_bases = [False] * num_bases
    total_cost = 0
    fib_heap = FibonacciHeap()
    fib_heap.add_node(0, 0)
    
    while fib_heap.node_count > 0:
        cost, base_index = fib_heap.get_min()
        if visited_bases[base_index]:
            continue
        visited_bases[base_index] = True
        total_cost += cost

        for other_base in range(num_bases):
            if not visited_bases[other_base]:
                edge_cost = min(
                    abs(bases_list[base_index][0] - bases_list[other_base][0]),
                    abs(bases_list[base_index][1] - bases_list[other_base][1])
                )
                fib_heap.add_node(edge_cost, other_base)

    return total_cost

# Function to measure algorithm performance
def evaluate_performance(algorithm, bases_list):
    start = time.time()
    result = algorithm(bases_list)
    end = time.time()
    return result, end - start

def main():
    # Obtain user input for bases
    bases_list = input_bases()

    print("Entered base coordinates:", bases_list)

    # Evaluate performance for each algorithm
    print("Testing Array-Based Implementation...")
    array_cost, array_duration = evaluate_performance(prim_mst_array_based, bases_list)
    print(f"Array-Based Implementation:")
    print(f"Total Cost: {array_cost}")
    print(f"Duration: {array_duration:.6f} seconds")

    print("\nTesting Binary Heap Implementation...")
    heap_cost, heap_duration = evaluate_performance(prim_mst_binary_heap, bases_list)
    print(f"Binary Heap Implementation:")
    print(f"Total Cost: {heap_cost}")
    print(f"Duration: {heap_duration:.6f} seconds")

    print("\nTesting Fibonacci Heap Implementation...")
    fib_heap_cost, fib_heap_duration = evaluate_performance(prim_mst_fib_heap, bases_list)
    print(f"Fibonacci Heap Implementation:")
    print(f"Total Cost: {fib_heap_cost}")
    print(f"Duration: {fib_heap_duration:.6f} seconds")

if __name__ == "__main__":
    main()
