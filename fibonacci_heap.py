# Fibonacci Heap implementation

import math


class FibonacciNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.degree = 0
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.mark = False


class FibonacciHeap:
    def __init__(self):
        self.minimum = None
        self.count = 0

    def _insert_root(self, node):
        node.parent = None

        if self.minimum is None:
            node.left = node.right = node
            self.minimum = node
        else:
            node.left = self.minimum
            node.right = self.minimum.right
            self.minimum.right.left = node
            self.minimum.right = node

            if node.key < self.minimum.key:
                self.minimum = node

    def insert(self, key, value=None):
        node = FibonacciNode(key, value)
        self._insert_root(node)
        self.count += 1
        return node

    def find_min(self):
        if self.minimum is None:
            return None

        return self.minimum.key, self.minimum.value

    def _remove_from_list(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def _add_child(self, parent, child):
        child.parent = parent
        child.mark = False

        if parent.child is None:
            child.left = child.right = child
            parent.child = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child

        parent.degree += 1

    def _link(self, child, parent):
        self._remove_from_list(child)
        self._add_child(parent, child)

    def _consolidate(self):
        roots = []
        current = self.minimum

        if current is None:
            return

        while True:
            roots.append(current)
            current = current.right
            if current == self.minimum:
                break

        degree_table = {}

        for node in roots:
            if node.parent is not None:
                continue

            current = node
            degree = current.degree

            while degree in degree_table:
                other = degree_table.pop(degree)

                if other.key < current.key:
                    current, other = other, current

                self._link(other, current)
                degree = current.degree

            degree_table[degree] = current

        self.minimum = None

        for node in degree_table.values():
            node.left = node.right = node
            self._insert_root(node)

    def extract_min(self):
        z = self.minimum

        if z is None:
            return None

        if z.child is not None:
            children = []
            current = z.child

            while True:
                children.append(current)
                current = current.right
                if current == z.child:
                    break

            for child in children:
                self._remove_from_list(child)
                child.parent = None
                child.left = child.right = child
                self._insert_root(child)

        next_root = z.right

        if next_root == z:
            self.minimum = None
        else:
            self._remove_from_list(z)
            self.minimum = next_root
            self._consolidate()

        self.count -= 1
        return z.key, z.value

    def _cut(self, node, parent):
        if node.right == node:
            parent.child = None
        else:
            node.left.right = node.right
            node.right.left = node.left

            if parent.child == node:
                parent.child = node.right

        parent.degree -= 1
        node.left = node.right = node
        node.parent = None
        node.mark = False
        self._insert_root(node)

    def _cascading_cut(self, node):
        parent = node.parent

        if parent is None:
            return

        if not node.mark:
            node.mark = True
        else:
            self._cut(node, parent)
            self._cascading_cut(parent)

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("New key cannot exceed current key.")

        node.key = new_key
        parent = node.parent

        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        if self.minimum is None or node.key < self.minimum.key:
            self.minimum = node

    def merge(self, other):
        if other.minimum is None:
            return

        if self.minimum is None:
            self.minimum = other.minimum
            self.count = other.count
        else:
            a = self.minimum
            b = other.minimum

            a_right = a.right
            b_left = b.left

            a.right = b
            b.left = a
            a_right.left = b_left
            b_left.right = a_right

            if other.minimum.key < self.minimum.key:
                self.minimum = other.minimum

            self.count += other.count

        other.minimum = None
        other.count = 0

    def __len__(self):
        return self.count


if __name__ == "__main__":
    heap = FibonacciHeap()

    events = [
        (5, "Link failure"),
        (2, "Router overheating"),
        (4, "Packet loss"),
        (1, "Core outage"),
        (3, "Low bandwidth")
    ]

    handles = {}

    for priority, event in events:
        handles[event] = heap.insert(priority, event)

    print("FIBONACCI HEAP")
    print("Minimum:", heap.find_min())

    heap.decrease_key(handles["Packet loss"], 0)
    print("After decrease-key:", heap.find_min())

    print("Extract minimum:", heap.extract_min())

    other = FibonacciHeap()
    other.insert(1, "Backup link failure")
    heap.merge(other)

    print("After merging heaps:", heap.find_min())

    while len(heap):
        print("Extracted:", heap.extract_min())