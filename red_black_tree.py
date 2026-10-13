# Red-Black Tree implementation

RED = True
BLACK = False


class Node:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, BLACK)
        self.root = self.NIL

    def search(self, key):
        current = self.root

        while current != self.NIL:
            if key == current.key:
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return False

    def insert(self, key):
        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL

        parent = self.NIL
        current = self.root

        while current != self.NIL:
            parent = current

            if key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent

        if parent == self.NIL:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node

        node.color = RED
        self._fix_insert(node)

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def _fix_insert(self, node):
        while node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right

                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)

                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._right_rotate(node.parent.parent)

            else:
                uncle = node.parent.parent.left

                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)

                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._left_rotate(node.parent.parent)

        self.root.color = BLACK
        self.root.parent = self.NIL


if __name__ == "__main__":
    tree = RedBlackTree()

    records = [101, 205, 110, 301, 222, 180, 150, 420, 390, 275]

    for record in records:
        tree.insert(record)

    print("RED-BLACK TREE RECORD INDEX")
    print("Inserted records:", records)
    print("Search 205:", tree.search(205))
    print("Search 999:", tree.search(999))
    print("Search 301:", tree.search(301))