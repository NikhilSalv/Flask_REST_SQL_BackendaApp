"""
I have pursued bruteforce approach to find the number of internal nodes.

"""

def find_internal_nodes_num_1(tree):
    """ 
    In this approach I have used a list creation operation to keep the track of number of children of each node.
    """
    n = len(tree)
    
    # A list is initialised to keep track of the number of children for each node
    children_count = [0] * n
    
    # Iterate through the tree list to count the number of children for each node
    for i in range(n):
        parent = tree[i]
        if parent != -1:
            children_count[parent] += 1
    
    # Count the number of internal nodes (nodes with at least one child)
    internal_nodes_count = sum(1 for count in children_count if count > 0)
    
    return internal_nodes_count




def find_internal_nodes_num_2(tree):
    """ 
    In this approach I have initialised a dictionary to keep the track of number of children of each node.
    """    
    children = {i: [] for i in range(len(tree))}
    
    # Fill the dictionary with child nodes
    for child, parent in enumerate(tree):
        if parent != -1:
            children[parent].append(child)
    
    # Count nodes that have at least one child
    internal_nodes_count = 0
    for node, child_list in children.items():
        if len(child_list) > 0:
            internal_nodes_count += 1
    
    return internal_nodes_count



my_tree = [4, 4, 1, 5, -1, 4, 5]
print(find_internal_nodes_num_1(my_tree)) 
print(find_internal_nodes_num_2(my_tree)) 



