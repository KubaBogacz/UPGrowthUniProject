"""
Example script to demonstrate UP-Growth algorithm visualization with small datasets.
This file contains a small example dataset embedded directly in the script
to make it easy to visualize the UP-Tree without computational complexity issues.
"""

from up_growth import UPTreeNode, UPTree, UPGrowthMiner
from visualization import visualize_up_tree, print_header_table
import os

def main():
    # Check for required libraries
    try:
        import networkx
        import matplotlib.pyplot as plt
        visualization_available = True
    except ImportError:
        print("Visualization libraries (networkx, matplotlib) not found.")
        print("Run 'pip install networkx matplotlib' for visualization support.")
        visualization_available = False
    
    # Small example dataset embedded directly in this script
    # Format: List of transactions, each transaction is a list of items
    transactions = [
        ['A', 'C', 'D'],
        ['A', 'C', 'E', 'G'],
        ['B', 'C', 'D', 'E'],
        ['B', 'C', 'D', 'E'],
        ['A', 'B', 'C', 'D', 'F', 'G', 'H'],
        ['B', 'E']
    ]
    
    # Corresponding utility values (internal utilities)
    utility_maps = [
        {'A': 5, 'C': 10, 'D': 2},
        {'A': 10, 'C': 6, 'E': 6, 'G': 5},
        {'B': 8, 'C': 3, 'D': 6, 'E': 3},
        {'B': 4, 'C': 3, 'D': 2, 'E': 3},
        {'A': 5, 'B': 2, 'C': 1, 'D': 2, 'F': 5, 'G': 1, 'H': 4},
        {'B': 4, 'E': 3}
    ]
    
    # Profit table (external utilities)
    profit_table = {'A': 5, 'B': 2, 'C': 1, 'D': 2, 'E': 3, 'F': 5, 'G': 1, 'H': 4}
    
    # Print transactions and utilities for verification
    print("\nExample Transaction Dataset:")
    for idx, transaction in enumerate(transactions):
        tu = sum(utility_maps[idx].values())
        print(f"T{idx+1}: {transaction}, Utility: {utility_maps[idx]}, TU: {tu}")
    
    print("\nProfit Table (External Utilities):")
    for item, profit in sorted(profit_table.items()):
        print(f"{item}: {profit}")
    
    # Set minimum utility threshold
    min_utility = 20  # Lower threshold for small example
    print(f"\nMinimum Utility Threshold: {min_utility}")
    
    # Construct UP-Tree separately to visualize it
    print("\nConstructing UP-Tree...")
    up_tree = UPTree()
    up_tree.construct_tree(transactions, utility_maps, min_utility)
    
    # Print UP-Tree structure
    up_tree.print_tree()
    
    # Print header table
    print_header_table(up_tree)
    
    # Visualize UP-Tree if visualization libraries are available
    if visualization_available:
        print("\nGenerating UP-Tree visualization...")
        visualize_up_tree(up_tree, f"UP-Tree Example (min_util={min_utility})", "up_tree_example_visualization.png")
    
    # Mine high utility itemsets
    print("\nMining high utility itemsets...")
    miner = UPGrowthMiner(min_utility)
    high_utility_itemsets = miner.mine(transactions, utility_maps, profit_table)
    
    # Display results
    print("\nHigh Utility Itemsets:")
    if high_utility_itemsets:
        for idx, (itemset, utility) in enumerate(sorted(high_utility_itemsets, key=lambda x: x[1], reverse=True)):
            print(f"{idx+1}. {itemset}, Utility: {utility}")
    else:
        print("No high utility itemsets found with the current minimum utility threshold.")
    
    # Display potential high utility itemsets (PHUIs)
    print("\nPotential High Utility Itemsets (PHUIs):")
    if miner.phuis:
        for idx, (itemset, estimated_utility) in enumerate(sorted(miner.phuis, key=lambda x: x[1], reverse=True)):
            print(f"{idx+1}. {itemset}, Estimated Utility: {estimated_utility}")
    else:
        print("No potential high utility itemsets found.")

if __name__ == "__main__":
    main()
