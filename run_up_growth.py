"""
Main script to run the UP-Growth algorithm on the example dataset.
"""

from up_growth import (UPTreeNode, UPTree, UPGrowthMiner, 
                      read_transaction_dataset, read_profit_table, 
                      calculate_utilities)

def main():
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
    for item, profit in profit_table.items():
        print(f"{item}: {profit}")
      # Set minimum utility threshold
    min_utility = 20  # Adjust this value as needed
    print(f"\nMinimum Utility Threshold: {min_utility}")
    
    # Mine high utility itemsets
    print("\nMining high utility itemsets...")
    miner = UPGrowthMiner(min_utility)
    high_utility_itemsets = miner.mine(transactions, utility_maps, profit_table)
    
    # Display results
    print("\nHigh Utility Itemsets:")
    for idx, (itemset, utility) in enumerate(high_utility_itemsets):
        print(f"{idx+1}. {itemset}, Utility: {utility}")
    
    # Optional: Display potential high utility itemsets (PHUIs)
    print("\nPotential High Utility Itemsets (PHUIs):")
    for idx, (itemset, estimated_utility) in enumerate(miner.phuis):
        print(f"{idx+1}. {itemset}, Estimated Utility: {estimated_utility}")

if __name__ == "__main__":
    main()
