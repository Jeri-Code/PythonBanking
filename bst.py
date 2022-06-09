from logging import root
from account import Account


class Node:
    # Node class python implementation from class
    def __init__(self, key: int, account=None):
        self.key = key
        self.account = account
        self.left_child = None
        self.right_child = None

    def is_leaf(self):
        return self.left_child is None and self.right_child is None

    def __str__(self):
        return str(self.key) + " " + str(self.account)


class BinaryTree:
    def __init__(self):
        self._count = 0
        self._root = None

    def size(self):
        return self._count

    def get(self, key: int):
        current_node = self._root
        while current_node is not None:
            if current_node.key == key:
                return current_node.account
            elif current_node.key > key:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child
        return None

    def put(self, key, account):
        # Set the root if nothing exists
        if self._count == 0:
            self._root = Node(key, account)
            self._count += 1
            return
        # Otherwise, transverse until a free spot is found
        current_node = self._root
        while True:
            # If the key is equal to the current node, then set it
            if current_node.key == key:
                current_node.account = account
                return
            # If the node is MORE than the key, create a new node on the left
            elif current_node.key > key:  # Questioning this but seems right
                if current_node.left_child is None:
                    new_node = Node(key, account)
                    current_node.left_child = new_node
                    break
                # If the node is more than the key, assign the left child as the current node
                else:
                    current_node = current_node.left_child  # Does NOT replace; just changes the searching node
            # If the left spots are all taken, then try the right
            else:
                if current_node.right_child is None:
                    new_node = Node(key, account)
                    current_node.right_child = new_node
                    break
                else:
                    current_node = current_node.right_child
        self._count += 1

    # Recursive display function traversing the BST and displaying balance for each account
    def display(self):
        curr = self._root
        self.display_helper(curr)

    def display_helper(self, subroot):
        if subroot is None:
            return

        self.display_helper(subroot.left_child)
        subroot.account.display_balance()
        self.display_helper(subroot.right_child)

    def __setitem__(self, key, data):
        self.put(key, data)

    def __getitem__(self, key):
        return self.get(key)
