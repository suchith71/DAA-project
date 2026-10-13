# B-Tree implementation

class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, degree=3):
        self.root = BTreeNode()
        self.degree = degree

    def search(self, key, node=None):
        if node is None:
            node = self.root

        i = 0

        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            return True

        if node.leaf:
            return False

        return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root

        if len(root.keys) == 2 * self.degree - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self.root = new_root

            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    def _split_child(self, parent, index):
        degree = self.degree
        child = parent.children[index]
        new_child = BTreeNode(leaf=child.leaf)

        middle_key = child.keys[degree - 1]

        new_child.keys = child.keys[degree:]
        child.keys = child.keys[:degree - 1]

        if not child.leaf:
            new_child.children = child.children[degree:]
            child.children = child.children[:degree]

        parent.children.insert(index + 1, new_child)
        parent.keys.insert(index, middle_key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(key)

            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1

            node.keys[i + 1] = key

        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1

            i += 1

            if len(node.children[i].keys) == 2 * self.degree - 1:
                self._split_child(node, i)

                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)


if __name__ == "__main__":
    tree = BTree(degree=3)

    records = [101, 205, 110, 301, 222, 180, 150, 420, 390, 275]

    for record in records:
        tree.insert(record)

    print("B-TREE RECORD INDEX")
    print("Inserted records:", records)
    print("Search 205:", tree.search(205))
    print("Search 999:", tree.search(999))
    print("Search 301:", tree.search(301))