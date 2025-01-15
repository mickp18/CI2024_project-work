import numpy as np
from print_tree import *
from visualize_tree import visualize_tree, display

class TreeNode:
    def __init__(self, value):
        self.value = value      # This can be an operator or operand
        self.left = None        # Left child
        self.right = None       # Right child
        self.coefficient = None # multiplicative coefficient for a variable
    
    def __copy__(self):
        return TreeNode(self.value, self.left, self.right, self.coefficient)

    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.value == other.value

    def get_nodes_from_node(self):
        """ 
        Returns a list of all nodes in the tree starting from the given node
        """
        nodes = []
        if self:
            nodes.append(self)
        if self.left:
            nodes.extend(self.left.get_nodes_from_node())
        if self.right:
            nodes.extend(self.right.get_nodes_from_node())
        return nodes
    
    def get_non_leaves_nodes_from_node(self):
        """
        Returns a list of all non leaf nodes in the tree starting from the given node
        """
        nodes = []
        if self and (self.left or self.right):
            nodes.append(self)
        if self.left:
            nodes.extend(self.left.get_non_leaves_nodes_from_node())
        if self.right:
            nodes.extend(self.right.get_non_leaves_nodes_from_node())
        return nodes
    
    def get_leaves_nodes_from_node(self):
        """
        Returns a list of all leaf nodes in the tree starting from the given node
        """
        nodes = []
        if self and not (self.left or self.right):
            nodes.append(self)
        if self.left:
            nodes.extend(self.left.get_leaves_nodes_from_node())
        if self.right:
            nodes.extend(self.right.get_leaves_nodes_from_node())
        return nodes
        
    def validate_tree_from_node(self, variables, binary_operators, unary_operators):
        """
        Returns True if the tree is syntactically correct without checking domain constraints of operators, False otherwise
        """
        if not self:
            return True
        
        if self.value in binary_operators:
            if not self.left or not self.right:
                return False  # Operators must have two children
            return self.left.validate_tree_from_node(variables, binary_operators, unary_operators) and self.right.validate_tree_from_node(variables, binary_operators, unary_operators)
        
        elif self.value in unary_operators:  # Allow unary operators
            if self.right and not self.left:
                return self.right.validate_tree_from_node(variables, binary_operators, unary_operators)
            return False  # Unary operators must have one child on the right
        
        # elif self.value in VARIABLES_MAP and isinstance(self.value, str):  # Allow variables
        elif self.value in variables: # or (self.value > -MAX_COEFFICIENT and self.value < MAX_COEFFICIENT):
            return True
        elif isinstance(self.value, float):
            return True
        else:
            return False  # Invalid value
    
    # (3 + 2) * (4 + 5)        Treenode (value = *, left = Treenode (value = +, left = 3, right = 2), right = Treenode (value = +, left = 4, right = 5))
    def evaluate_tree_from_node(self, variables_map, binary_operators_map, unary_operators_map):
        """
        Returns the value of the expression represented by the tree starting form a specific node
        """
        if not self:
            raise ValueError("Cannot evaluate an empty tree.")
        
        # Check if it's a binary operator
        if self.value in binary_operators_map:
            left_val = self.left.evaluate_tree_from_node(variables_map, binary_operators_map, unary_operators_map)
            right_val = self.right.evaluate_tree_from_node(variables_map, binary_operators_map, unary_operators_map)
            return binary_operators_map[self.value](left_val, right_val)
        
        # Check if it's a unary operator
        elif self.value in unary_operators_map:
            right_val = self.right.evaluate_tree_from_node(variables_map, binary_operators_map, unary_operators_map) # Typically applies to right child
            return unary_operators_map[self.value](right_val)  # Correct unary application
        
        # Check if it's a variable
        elif self.value in variables_map:
            # return VARIABLES_MAP[self.value]  # Lookup the variable value
            return np.multiply(self.coefficient, variables_map[self.value])  # Lookup the variable value
        
        # Check if it's a numeric constant or coefficient
        elif isinstance(self.value, (int, float)):
            return self.value  # Return as-is for numeric leaf selfs
        
        # If none of the above, it's an error
        else:
            raise ValueError(f"Invalid self value: {self.value}")

    def print_tree_from_node(self, variables_map):
        print_expr(self, variables_map)

    def print_tree_values_from_node(self, variables_map, binary_operators_map, unary_operators_map):
        print_expr_values(self, variables_map, binary_operators_map, unary_operators_map)

    def draw_tree_from_node(self):
        display(visualize_tree(self))