"""
UP-Growth: An Efficient Algorithm for High Utility Itemset Mining

Implementation based on the paper by Vincent S. Tseng et al.
"""

class UPTreeNode:
    """Node structure for the UP-Tree."""
    
    def __init__(self, item=None, count=0, parent=None):
        """
        Initialize a UP-Tree node.
        
        Args:
            item: The item represented by this node
            count: The support count of the node
            parent: The parent node
        """
        self.item = item  # Item name
        self.count = count  # Support count
        self.node_utility = 0  # Node utility (nu)
        self.parent = parent  # Parent node reference
        self.children = {}  # Dictionary of child nodes
        self.next = None  # Reference to the next node with same item (horizontal link)

class UPTree:
    """Utility Pattern Tree structure for UP-Growth algorithm."""
    
    def __init__(self):
        """Initialize an empty UP-Tree."""
        # Root node with no item
        self.root = UPTreeNode()
        # Header table to store the first occurrence of each item
        self.header_table = {}
        # Item TWU values
        self.item_twu = {}
    
    def add_transaction(self, transaction, utility_map, transaction_utility):
        """
        Add a transaction to the UP-Tree.
        
        Args:
            transaction: List of items in the transaction
            utility_map: Dictionary mapping items to their utilities in this transaction
            transaction_utility: The total utility of the transaction
        """
        current_node = self.root
        remaining_utility = transaction_utility
        
        for item in transaction:
            # Subtract current item's utility from remaining utility
            remaining_utility -= utility_map[item]
            
            # Check if item is in children of current node
            if item in current_node.children:
                child = current_node.children[item]
                # Increment count
                child.count += 1
                # Add remaining utility to node utility (DGN strategy)
                child.node_utility += remaining_utility
            else:
                # Create a new node
                child = UPTreeNode(item=item, count=1, parent=current_node)
                child.node_utility = remaining_utility
                current_node.children[item] = child
                
                # Update header table
                if item in self.header_table:
                    # Add to horizontal node links
                    prev = self.header_table[item]
                    while prev.next is not None:
                        prev = prev.next
                    prev.next = child
                else:
                    # First occurrence of this item
                    self.header_table[item] = child
            
            current_node = child
    
    def construct_tree(self, transactions, utility_maps, min_utility):
        """
        Construct the UP-Tree from a set of transactions.
        
        Args:
            transactions: List of transactions where each transaction is a list of items
            utility_maps: List of utility maps for each transaction
            min_utility: Minimum utility threshold
        """
        # First scan: compute TWU for each item
        transaction_utilities = []
        for idx, transaction in enumerate(transactions):
            tu = sum(utility_maps[idx].values())
            transaction_utilities.append(tu)
            
            # Update TWU of each item
            for item in transaction:
                if item in self.item_twu:
                    self.item_twu[item] += tu
                else:
                    self.item_twu[item] = tu
        
        # Identify unpromising items (items with TWU < min_utility)
        promising_items = {item for item, twu in self.item_twu.items() if twu >= min_utility}
        
        # Second scan: construct UP-Tree
        for idx, transaction in enumerate(transactions):
            # Keep only promising items in the transaction
            filtered_transaction = [item for item in transaction if item in promising_items]
            
            # Sort items by TWU in descending order
            filtered_transaction.sort(key=lambda x: self.item_twu[x], reverse=True)
            
            # Skip empty transactions
            if not filtered_transaction:
                continue
            
            # Create a utility map for the filtered transaction
            filtered_utility_map = {item: utility_maps[idx][item] for item in filtered_transaction}
            
            # Compute transaction utility for the filtered transaction
            filtered_tu = sum(filtered_utility_map.values())
            
            # Add transaction to the tree
            self.add_transaction(filtered_transaction, filtered_utility_map, filtered_tu)
            
    def print_tree(self, node=None, indent=""):
        """Print the tree structure (for debugging)."""
        if node is None:
            node = self.root
            print("UP-Tree:")
        
        # Print current node
        if node.item is not None:
            print(f"{indent}Item: {node.item}, Count: {node.count}, Utility: {node.node_utility}")
        else:
            print(f"{indent}Root")
        
        # Print children
        for child in node.children.values():
            self.print_tree(child, indent + "  ")


class UPGrowthMiner:
    """Implementation of the UP-Growth algorithm for mining high utility itemsets."""
    
    def __init__(self, min_utility=0):
        """
        Initialize the UP-Growth miner.
        
        Args:
            min_utility: Minimum utility threshold
        """
        self.min_utility = min_utility
        self.phuis = []  # Potential high utility itemsets
        self.huis = []   # High utility itemsets (final result)
        
    def mine(self, transactions, utility_maps, profit_table):
        """
        Mine high utility itemsets using the UP-Growth algorithm.
        
        Args:
            transactions: List of transactions where each transaction is a list of items
            utility_maps: List of utility maps for each transaction
            profit_table: Dictionary mapping items to their external utilities (profit values)
            
        Returns:
            List of high utility itemsets with their utilities
        """
        # Construct initial UP-Tree
        up_tree = UPTree()
        up_tree.construct_tree(transactions, utility_maps, self.min_utility)
        
        # Print initial tree (for debugging)
        # up_tree.print_tree()
        
        # Mine patterns from the UP-Tree
        self._mine_tree(up_tree, [])
        
        # Phase 2: Calculate exact utilities and filter true high utility itemsets
        self._identify_high_utility_itemsets(transactions, utility_maps, profit_table)
        
        return self.huis
    
    def _mine_tree(self, tree, prefix):
        """
        Recursively mine patterns from a UP-Tree (UP-Growth algorithm).
        
        Args:
            tree: The UP-Tree to mine
            prefix: Current prefix itemset
        """
        # Process each item in the header table
        for item, node in sorted(tree.header_table.items()):
            # Create new prefix by combining current prefix with the current item
            new_prefix = prefix + [item]
            
            # Calculate estimated utility of the new pattern
            estimated_utility = self._calculate_path_utility(node)
            
            # Add as a potential high utility itemset if its estimated utility is high enough
            if estimated_utility >= self.min_utility:
                self.phuis.append((new_prefix, estimated_utility))
            
            # Construct conditional pattern base
            path_utility_dict = {}
            conditional_pattern_base = []
            conditional_utility_maps = []
            
            # Create a local copy of the node to follow horizontal links
            current_node = node
            
            # Follow horizontal links to find all occurrences of the item
            while current_node is not None:
                # Get path from root to this node (excluding the item itself)
                path = self._get_path(current_node.parent)
                if path:
                    path_support = current_node.count
                    path_utility = current_node.node_utility
                    
                    conditional_pattern_base.append(path)
                    
                    # Create utility map for the conditional pattern
                    utility_map = {}
                    remaining_utility = path_utility
                    
                    # Calculate utilities for each item in the path
                    # (applying DLU and DLN strategies)
                    for path_item in reversed(path):
                        # Estimate utility using path information
                        if path_item in utility_map:
                            utility_map[path_item] += (remaining_utility * path_support)
                        else:
                            utility_map[path_item] = (remaining_utility * path_support)
                        
                        # Reduce remaining utility (DLN strategy)
                        if path_item in path_utility_dict:
                            remaining_utility -= (path_utility_dict[path_item] / path_support)
                    
                    conditional_utility_maps.append(utility_map)
                  # Move to the next occurrence via horizontal link
                current_node = current_node.next
            
            # Skip if no conditional patterns
            if not conditional_pattern_base:
                continue
            
            # Construct conditional UP-Tree
            conditional_tree = UPTree()
            conditional_tree.construct_tree(conditional_pattern_base, conditional_utility_maps, self.min_utility)
            
            # Recursively mine the conditional UP-Tree with the new prefix
            if conditional_tree.root.children:
                self._mine_tree(conditional_tree, new_prefix)
    
    def _get_path(self, node):
        """
        Get the path from root to the given node (excluding the node itself).
        
        Args:
            node: The target node
            
        Returns:
            List of items in the path
        """
        path = []
        while node.parent is not None:
            path.append(node.item)
            node = node.parent
        return path[::-1]  # Reverse to get path from root to node
    
    def _calculate_path_utility(self, node):
        """
        Calculate the estimated utility of a pattern using node information.
        
        Args:
            node: The node representing the last item in the pattern
            
        Returns:
            Estimated utility of the pattern
        """
        utility = 0
        # Follow horizontal links to find all occurrences
        while node is not None:
            utility += node.node_utility
            node = node.next
        return utility
    
    def _identify_high_utility_itemsets(self, transactions, utility_maps, profit_table):
        """
        Identify true high utility itemsets from PHUIs by calculating exact utilities.
        
        Args:
            transactions: List of transactions
            utility_maps: List of utility maps for each transaction
            profit_table: Dictionary mapping items to their external utilities
        """
        for pattern, _ in self.phuis:
            exact_utility = self._calculate_exact_utility(pattern, transactions, utility_maps)
            if exact_utility >= self.min_utility:
                self.huis.append((pattern, exact_utility))
    
    def _calculate_exact_utility(self, pattern, transactions, utility_maps):
        """
        Calculate the exact utility of an itemset in the database.
        
        Args:
            pattern: The itemset
            transactions: List of transactions
            utility_maps: List of utility maps for each transaction
            
        Returns:
            Exact utility of the itemset
        """
        total_utility = 0
        pattern_set = set(pattern)
        
        for idx, transaction in enumerate(transactions):
            # Check if transaction contains the pattern
            if pattern_set.issubset(set(transaction)):
                # Sum utilities of all items in the pattern
                utility = sum(utility_maps[idx][item] for item in pattern)
                total_utility += utility
                
        return total_utility


def read_transaction_dataset(file_path):
    """
    Read transaction dataset from a file.
    
    Expected format:
    Each line represents a transaction with items and quantities separated by spaces.
    Example: "A:1 B:2 C:3" represents a transaction with item A (quantity 1), B (quantity 2), and C (quantity 3).
    
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
            if not line or line.startswith('#'):
                continue
                
            items = line.split()
            transaction = []
            utility_map = {}
            
            for item_qty in items:
                try:
                    item, qty = item_qty.split(':')
                    qty = int(qty)
                    transaction.append(item)
                    utility_map[item] = qty  # Internal utility is the quantity
                except ValueError:
                    print(f"Warning: Skipping invalid item format: {item_qty}")
            
            transactions.append(transaction)
            utility_maps.append(utility_map)
    
    return transactions, utility_maps


def read_profit_table(file_path):
    """
    Read profit table from a file.
    
    Expected format:
    Each line contains an item and its profit value separated by a space.
    Example: "A 5" means item A has a profit (external utility) of 5.
    
    Args:
        file_path: Path to the profit table file
        
    Returns:
        Dictionary mapping items to their external utilities (profit values)
    """
    profit_table = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines and comment lines
            if not line or line.startswith('#'):
                continue
                
            try:
                item, profit = line.split()
                profit_table[item] = int(profit)
            except ValueError:
                print(f"Warning: Skipping invalid profit table entry: {line}")
    
    return profit_table


def calculate_utilities(transactions, utility_maps, profit_table):
    """
    Calculate total utilities for transactions based on internal utilities and profit table.
    
    Args:
        transactions: List of transactions
        utility_maps: List of internal utility maps
        profit_table: Dictionary mapping items to their external utilities
        
    Returns:
        List of updated utility maps with total utilities (internal × external)
    """
    updated_utility_maps = []
    
    for idx, transaction in enumerate(transactions):
        updated_utility_map = {}
        for item in transaction:
            # Total utility = internal utility × external utility
            internal_utility = utility_maps[idx][item]
            external_utility = profit_table[item]
            updated_utility_map[item] = internal_utility * external_utility
        
        updated_utility_maps.append(updated_utility_map)
    
    return updated_utility_maps
