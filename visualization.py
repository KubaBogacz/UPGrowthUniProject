"""
Visualization helpers for UP-Growth algorithm.
"""

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    visualization_available = True
except ImportError:
    visualization_available = False

from up_growth import UPTree, UPTreeNode

def visualize_up_tree(tree, title="UP-Tree Visualization"):
    """
    Visualize the UP-Tree using networkx and matplotlib.
    
    Args:
        tree: UPTree instance to visualize
        title: Title for the plot
    """
    if not visualization_available:
        print("Visualization libraries not available. Please install networkx and matplotlib.")
        return
        
    G = nx.DiGraph()
    
    # Helper function to add nodes recursively
    def add_nodes(node, parent_id=None):
        if node.item is None:
            node_id = "Root"
            node_label = "Root"
        else:
            node_id = f"{node.item}_{id(node)}"
            node_label = f"{node.item}\ncount:{node.count}\nnu:{node.node_utility}"
        
        G.add_node(node_id, label=node_label)
        
        if parent_id is not None:
            G.add_edge(parent_id, node_id)
        
        for child in node.children.values():
            add_nodes(child, node_id)
    
    # Add nodes starting from root
    add_nodes(tree.root)
      # Try to use graphviz layout if available
    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except (ImportError, AttributeError):
        print("pygraphviz not available, using spring layout instead")
        pos = nx.spring_layout(G)
        
    # Draw the graph
    plt.figure(figsize=(12, 10))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha=0.8)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    
    # Draw labels
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    
    # Add horizontal links with dotted lines
    horizontal_links = []
    for item, node in tree.header_table.items():
        current = node
        while current.next is not None:
            source = f"{current.item}_{id(current)}"
            target = f"{current.next.item}_{id(current.next)}"
            horizontal_links.append((source, target))
            current = current.next
    
    if horizontal_links:
        # Create a new graph for horizontal links
        H = nx.DiGraph()
        H.add_edges_from(horizontal_links)
        nx.draw_networkx_edges(H, pos, width=1.0, alpha=0.5, edge_color='r', style='dashed')
    
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("up_tree_visualization.png")
    plt.close()
    
    print(f"UP-Tree visualization saved as 'up_tree_visualization.png'")


def print_header_table(tree):
    """
    Print the header table of a UP-Tree.
    
    Args:
        tree: UPTree instance
    """
    print("\nHeader Table:")
    for item, node in sorted(tree.header_table.items()):
        current = node
        occurrences = []
        while current is not None:
            occurrences.append(f"(count:{current.count}, nu:{current.node_utility})")
            current = current.next
        print(f"Item: {item}, TWU: {tree.item_twu.get(item, 'N/A')}, Occurrences: {' -> '.join(occurrences)}")
