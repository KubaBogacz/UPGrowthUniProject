"""
Parsers for the UP-Growth algorithm with the new data format.
"""

def read_item_names(file_path):
    """
    Read item names file in the format:
    @ITEM=item_id=item_name
    
    Args:
        file_path: Path to the item names file
        
    Returns:
        Dictionary mapping item IDs to their names
    """
    item_names = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines, comment lines, and header
            if not line or line.startswith('#') or line.startswith('//') or line.startswith('@CONVERTED'):
                continue
                
            if line.startswith('@ITEM='):
                try:
                    # Remove '@ITEM=' prefix and split by '='
                    parts = line[6:].split('=', 1)
                    if len(parts) == 2:
                        item_id, item_name = parts
                        item_names[item_id] = item_name
                except Exception as e:
                    print(f"Warning: Invalid item name format: {line}, Error: {e}")
    
    return item_names


def read_transactions_new_format(file_path):
    """
    Read transaction dataset from a file with the new format.
    
    Expected format:
    item_1 item_2 ... item_n : transaction_utility : utility_1 utility_2 ... utility_n
    
    Args:
        file_path: Path to the transaction dataset file
        
    Returns:
        transactions: List of transactions where each transaction is a list of items
        utility_maps: List of utility maps for each transaction (internal utilities)
    """
    transactions = []
    utility_maps = []
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and comment lines
            if not line or line.startswith('#') or line.startswith('//'):
                continue
            
            try:
                # Split the line into three parts: items, transaction_utility, utilities
                parts = line.split(':')
                if len(parts) != 3:
                    print(f"Warning: Skipping invalid transaction format (expected 3 parts): {line}")
                    continue
                
                items_str, transaction_utility_str, utilities_str = parts
                
                # Parse items
                items = items_str.split()
                
                # Parse transaction utility (not needed for our algorithm)
                transaction_utility = int(transaction_utility_str)
                
                # Parse utilities
                utilities = utilities_str.split()
                
                # Create transaction and utility map
                transaction = []
                utility_map = {}
                
                # Check if the number of items matches the number of utilities
                if len(items) != len(utilities):
                    print(f"Warning: Number of items ({len(items)}) doesn't match number of utilities ({len(utilities)}) in: {line}")
                    continue
                
                # Map items to their utilities
                for i, item in enumerate(items):
                    utility = int(utilities[i])
                    transaction.append(item)
                    utility_map[item] = utility
                
                transactions.append(transaction)
                utility_maps.append(utility_map)
                
            except Exception as e:
                print(f"Warning: Error parsing transaction: {line}, Error: {e}")
    
    return transactions, utility_maps


def create_profit_table(transactions, utility_maps):
    """
    Create a profit table (external utilities) from the transactions.
    In our case, since the utility is already provided, we'll use a unit profit of 1 for each item.
    
    Args:
        transactions: List of transactions
        utility_maps: List of utility maps
        
    Returns:
        Dictionary mapping items to their external utilities (profit values)
    """
    profit_table = {}
    
    # Find all unique items
    all_items = set()
    for transaction in transactions:
        all_items.update(transaction)
    
    # Set profit to 1 for all items (since utilities are already provided)
    for item in all_items:
        profit_table[item] = 1
    
    return profit_table
