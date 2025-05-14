"""
Enhanced version of the run_up_growth script with visualization.
"""

from up_growth import (UPTreeNode, UPTree, UPGrowthMiner, 
                      read_transaction_dataset, read_profit_table, 
                      calculate_utilities)
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
        print("Run 'pip install networkx matplotlib pydot' for visualization support.")
        visualization_available = False
    
    # Read dataset
    print("Reading dataset...")
    transactions, internal_utility_maps = read_transaction_dataset("example_transactions.txt")
    profit_table = read_profit_table("example_profit_table.txt")
    
    # Calculate utilities (internal utility × external utility)
    utility_maps = calculate_utilities(transactions, internal_utility_maps, profit_table)
    
    # Print transactions and utilities for verification
    print("\nTransaction Dataset:")
    for idx, transaction in enumerate(transactions):
        tu = sum(utility_maps[idx].values())
        print(f"T{idx+1}: {transaction}, Utility: {utility_maps[idx]}, TU: {tu}")
    
    print("\nProfit Table (External Utilities):")
    for item, profit in sorted(profit_table.items()):
        print(f"{item}: {profit}")
      # Set minimum utility threshold
    min_utility = 20  # Adjust this value as needed
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
        visualize_up_tree(up_tree, f"UP-Tree (min_util={min_utility})")
    
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
    
    # Optional: Display potential high utility itemsets (PHUIs)
    print("\nPotential High Utility Itemsets (PHUIs):")
    if miner.phuis:
        for idx, (itemset, estimated_utility) in enumerate(sorted(miner.phuis, key=lambda x: x[1], reverse=True)):
            print(f"{idx+1}. {itemset}, Estimated Utility: {estimated_utility}")
    else:
        print("No potential high utility itemsets found.")

if __name__ == "__main__":
    main()
