# UP-Growth Algorithm Implementation

This repository contains a Python implementation of the UP-Growth algorithm for high utility itemset mining as described in the paper "UP-Growth: An Efficient Algorithm for High Utility Itemset Mining" by Vincent S. Tseng et al.

## Overview

UP-Growth (Utility Pattern Growth) is an efficient algorithm for mining high utility itemsets from transactional databases. It uses a tree-based data structure called UP-Tree (Utility Pattern Tree) to maintain utility information and employs several strategies to reduce the search space.

## Repository Structure

- **Core Implementation**
  - `up_growth.py`: Contains the main algorithm implementation (UPTreeNode, UPTree, UPGrowthMiner)
  - `parsers.py`: Data format parsers for transaction datasets and item name mappings

- **Scripts**
  - `run_up_growth.py`: Main script for processing large datasets
  - `demo_visualization.py`: Example script with visualization for small datasets

- **Utilities**
  - `visualization.py`: Visualization tools for UP-Tree structure

- **Data**
  - `example_transactions.txt`: Example transaction dataset
  - `item_names.txt`: Item ID to name mappings
  - `ecommerce_utility_no_timestamps.txt`: Larger dataset for testing

## Key Features

1. **Efficient Data Structures**
   - UP-Tree with header table and node links
   - Transaction-weighted utilization (TWU) calculations

2. **Optimization Strategies**
   - DGU: Discarding Global Unpromising items
   - DGN: Decreasing Global Node utilities
   - DLU: Discarding Local Unpromising items
   - DLN: Decreasing Local Node utilities

3. **Two-Phase Mining**
   - Phase 1: Generate potential high utility itemsets (PHUIs)
   - Phase 2: Identify true high utility itemsets (HUIs)

4. **Support for Multiple Data Formats**
   - Custom transaction format
   - Item name mapping support

## Usage

### Processing Large Datasets

```bash
python run_up_growth.py
```

This will:
- Read transaction data and item names
- Mine high utility itemsets based on the defined threshold
- Output results to console and save to a file

### Small Dataset Visualization

```bash
python demo_visualization.py
```

This provides a visualization of the UP-Tree structure using a small example dataset.

## Data Formats

### Transaction Format

```
item_1 item_2 ... item_n : transaction_utility : utility_1 utility_2 ... utility_n
```

Example:
```
21730 22752 71053 : 13912 : 2550 1530 2034
```

### Item Names Format

```
@ITEM=item_id=item_name
```

Example:
```
@ITEM=90112=PINK DOLLY HAIR CLIPS
```

## Performance Considerations

- Data processing and visualization are separated for better performance with large datasets
- The minimum utility threshold can be adjusted to control result size
- For very large datasets, consider increasing the threshold value

## Requirements

```
# Core
numpy

# For visualization
matplotlib
networkx
pydot  # For graphviz layout support
```

## Installation

```bash
pip install -r requirements.txt
```

## References

- Tseng, V. S., Shie, B.-E., Wu, C.-W., & Yu, P. S. (2013). "Efficient algorithms for mining high utility itemsets from transactional databases." IEEE Transactions on Knowledge and Data Engineering, 25(8), 1772-1786.
