"""
Main script to run the UP-Growth algorithm on large datasets.
This file focuses on efficient data processing without visualization 
which would be too computationally complex for large datasets.
"""

from up_growth import UPGrowthMiner
from parsers import read_item_names, read_transactions_new_format, create_profit_table
import time
import os

def main():
    start_time = time.time()
    
    # Set file paths - can be changed to process different datasets
    transactions_file = "example_transactions.txt"
    item_names_file = "item_names.txt"
    
    # Read dataset with the new format
    print(f"Reading dataset from {transactions_file}...")
    transactions, internal_utility_maps = read_transactions_new_format(transactions_file)
    print(f"Read {len(transactions)} transactions with {sum(len(t) for t in transactions)} items total")
    
    # Create profit table (external utilities will be set to 1 for each item)
    profit_table = create_profit_table(transactions, internal_utility_maps)
    print(f"Created profit table with {len(profit_table)} items")
    
    # Read item names (for display purposes)
    try:
        item_names = read_item_names(item_names_file)
        print(f"Read {len(item_names)} item names")
    except Exception as e:
        print(f"Warning: Could not read item names: {e}")
        item_names = {}    # Calculate utilities (no need to multiply by external utility since we're setting it to 1)
    # Just use the internal utilities directly
    utility_maps = internal_utility_maps
    
    # Set minimum utility threshold
    min_utility = 20000  # Higher threshold for real data
    print(f"\nMinimum Utility Threshold: {min_utility}")
    
    # Start mining process
    print("\nMining high utility itemsets...")
    mining_start_time = time.time()
    miner = UPGrowthMiner(min_utility)
    high_utility_itemsets = miner.mine(transactions, utility_maps, profit_table)
    mining_time = time.time() - mining_start_time
    
    # Display results with item names if available
    print(f"\nMining completed in {mining_time:.2f} seconds")
    print(f"Found {len(high_utility_itemsets)} high utility itemsets")
    print(f"Found {len(miner.phuis)} potential high utility itemsets (PHUIs)")
    
    # Save results to file
    results_file = "high_utility_itemsets.txt"
    print(f"\nSaving high utility itemsets to {results_file}...")
    
    with open(results_file, "w") as f:
        f.write(f"# High Utility Itemsets (min_utility={min_utility})\n")
        f.write(f"# Total items: {len(high_utility_itemsets)}\n")
        f.write(f"# Format: Rank. [ItemID (ItemName)] Utility\n\n")
        
        if high_utility_itemsets:
            for idx, (itemset, utility) in enumerate(sorted(high_utility_itemsets, key=lambda x: x[1], reverse=True)):
                # Format with item names if available
                if item_names:
                    item_names_str = ", ".join([f"{item} ({item_names.get(item, 'Unknown')})" for item in itemset])
                    f.write(f"{idx+1}. [{item_names_str}], Utility: {utility}\n")
                else:
                    f.write(f"{idx+1}. {itemset}, Utility: {utility}\n")
        else:
            f.write("No high utility itemsets found with the current minimum utility threshold.\n")
    
    # Display top results
    if high_utility_itemsets:
        print("\nTop 10 High Utility Itemsets:")
        for idx, (itemset, utility) in enumerate(sorted(high_utility_itemsets, key=lambda x: x[1], reverse=True)[:10]):
            # Show item names if available
            if item_names:
                item_names_str = ", ".join([f"{item} ({item_names.get(item, 'Unknown')})" for item in itemset])
                print(f"{idx+1}. [{item_names_str}], Utility: {utility}")
            else:
                print(f"{idx+1}. {itemset}, Utility: {utility}")
    else:
        print("\nNo high utility itemsets found with the current minimum utility threshold.")
    
    # Show summary
    total_time = time.time() - start_time
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    
    # Optional: Display potential high utility itemsets (PHUIs)
    print("\nPotential High Utility Itemsets (PHUIs) - Top 10:")
    if miner.phuis:
        for idx, (itemset, estimated_utility) in enumerate(sorted(miner.phuis, key=lambda x: x[1], reverse=True)[:10]):
            # Show item names if available
            if item_names:
                item_names_str = ", ".join([f"{item} ({item_names.get(item, 'Unknown')})" for item in itemset])
                print(f"{idx+1}. [{item_names_str}], Estimated Utility: {estimated_utility}")
            else:
                print(f"{idx+1}. {itemset}, Estimated Utility: {estimated_utility}")
    else:
        print("No potential high utility itemsets found.")

if __name__ == "__main__":
    main()
