# Binomial Heap implementation

class BinomialNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None


class BinomialHeap:
    def __init__(self):
        self.head = None

    def _merge_roots(self, h1, h2):
        dummy = BinomialNode(0)
        tail = dummy

        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling

        tail.sibling = h1 if h1 else h2
        return dummy.sibling

    def _link(self, child, parent):
        child.parent = parent
        child.sibling = parent.child
        parent.child = child
        parent.degree += 1

    def _union(self, other_head):
        self.head = self._merge_roots(self.head, other_head)

        if not self.head:
            return

        previous = None
        current = self.head
        next_node = current.sibling

        while next_node:
            if (
                current.degree != next_node.degree
                or (
                    next_node.sibling
                    and next_node.sibling.degree == current.degree
                )
            ):
                previous = current
                current = next_node
            elif current.key <= next_node.key:
                current.sibling = next_node.sibling
                self._link(next_node, current)
            else:
                if previous is None:
                    self.head = next_node
                else:
                    previous.sibling = next_node

                self._link(current, next_node)
                current = next_node

            next_node = current.sibling

    def insert(self, key, value=None):
        node = BinomialNode(key, value)
        temporary = BinomialHeap()
        temporary.head = node
        self._union(temporary.head)

    def find_min(self):
        if not self.head:
            return None

        current = self.head
        minimum = current

        while current:
            if current.key < minimum.key:
                minimum = current
            current = current.sibling

        return minimum.key, minimum.value

    def extract_min(self):
        if not self.head:
            return None

        previous_min = None
        minimum = self.head
        previous = None
        current = self.head

        while current:
            if current.key < minimum.key:
                minimum = current
                previous_min = previous

            previous = current
            current = current.sibling

        if previous_min:
            previous_min.sibling = minimum.sibling
        else:
            self.head = minimum.sibling

        child = minimum.child
        reversed_children = None

        while child:
            next_child = child.sibling
            child.sibling = reversed_children
            child.parent = None
            reversed_children = child
            child = next_child

        self._union(reversed_children)

        return minimum.key, minimum.value

    def merge(self, other):
        self._union(other.head)
        other.head = None


if __name__ == "__main__":
    heap = BinomialHeap()

    events = [
        (5, "Link failure"),
        (2, "Router overheating"),
        (4, "Packet loss"),
        (1, "Core outage"),
        (3, "Low bandwidth")
    ]

    for priority, event in events:
        heap.insert(priority, event)

    print("BINOMIAL HEAP")
    print("Minimum priority:", heap.find_min())
    print("Extract minimum:", heap.extract_min())
    print("Next minimum:", heap.find_min())

    other = BinomialHeap()
    other.insert(0, "Critical network failure")
    heap.merge(other)

    print("After merging heaps:", heap.extract_min())