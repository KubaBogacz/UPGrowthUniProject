# UP-Growth Algorithm Implementation

This repository contains an implementation of the UP-Growth algorithm for high utility itemset mining, based on the academic paper "UP-Growth: An Efficient Algorithm for High Utility Itemset Mining" by Vincent S. Tseng et al.

## Overview

The UP-Growth algorithm is designed to efficiently mine high utility itemsets from transaction databases. It uses a tree-based data structure called UP-Tree (Utility Pattern Tree) to maintain the information about high utility itemsets.

## Files and Structure

- `up_growth.py`: Core implementation of the UP-Growth algorithm
- `parsers.py`: Parsers for different data formats including transaction datasets and item names
- `visualization.py`: Utilities for visualizing the UP-Tree structure
- `run_up_growth.py`: Main script for running the algorithm on large datasets
- `demo_visualization.py`: Example script for visualizing small datasets

## How to Use

### Processing Large Datasets

For processing large datasets, use the `run_up_growth.py` script:

```
python run_up_growth.py
```

This script:
1. Reads transaction data from the specified file
2. Processes the data using the UP-Growth algorithm
3. Outputs high utility itemsets to a file and displays a summary

### Visualizing Small Datasets

For visualizing UP-Trees with small datasets, use the `demo_visualization.py` script:

```
python demo_visualization.py
```

This script:
1. Uses a small embedded example dataset
2. Constructs and visualizes the UP-Tree
3. Mines high utility itemsets
4. Displays the results

## Data Formats

### Transaction Format

The implementation supports the following transaction format:
```
item_1 item_2 ... item_n : transaction_utility : utility_1 utility_2 ... utility_n
```

Example:
```
21730 22752 71053 : 13912 : 2550 1530 2034
```

### Item Names Format

Item names are read from a file with the following format:
```
@ITEM=item_id=item_name
```

Example:
```
@ITEM=90112=PINK DOLLY HAIR CLIPS
```

## Performance Considerations

- Visualization is separated from data processing due to computational complexity
- For large datasets, the visualization should be disabled
- The minimum utility threshold can be adjusted to control the number of generated itemsets

## Requirements

- Python 3.6+
- Required packages: networkx, matplotlib (for visualization only)

## References

- Vincent S. Tseng et al. "UP-Growth: An Efficient Algorithm for High Utility Itemset Mining"
