# UP-Growth Algorithm Implementation

This repository contains a Python implementation of the UP-Growth algorithm for high utility itemset mining as described in the paper "UP-Growth: An Efficient Algorithm for High Utility Itemset Mining" by Vincent S. Tseng et al.

## Overview

UP-Growth (Utility Pattern Growth) is an efficient algorithm for mining high utility itemsets from transactional databases. It uses a special tree structure called UP-Tree (Utility Pattern Tree) to maintain the utility information of the patterns and uses several strategies to effectively reduce the search space.

## Components

- `up_growth.py`: Core implementation of the UP-Growth algorithm
  - `UPTreeNode`: Node structure for the UP-Tree
  - `UPTree`: Utility Pattern Tree structure
  - `UPGrowthMiner`: Main implementation of the mining algorithm
  - Utility functions for reading datasets and calculating utilities

- `run_up_growth.py`: Script to run the algorithm on an example dataset

- Example dataset:
  - `example_transactions.txt`: Sample transaction dataset
  - `example_profit_table.txt`: External utility (profit) values for items

## Key Features

1. **Utility Calculations**:
   - Internal utility (e.g., quantity of items in transactions)
   - External utility (e.g., profit or unit price of items)
   - Transaction utility (TU)
   - Transaction-weighted utilization (TWU)

2. **UP-Tree Construction**:
   - Two-phase scan of the database
   - Efficient representation of utility information
   - Header table with horizontal node links

3. **Mining Strategies**:
   - DGU (Discarding Global Unpromising items)
   - DGN (Decreasing Global Node utilities)
   - DLU (Discarding Local Unpromising items)
   - DLN (Decreasing Local Node utilities)

4. **Two-Phase Mining**:
   - Phase 1: Mine potential high utility itemsets (PHUIs)
   - Phase 2: Identify true high utility itemsets (HUIs)

## Usage

1. Run the example script:
   ```
   python run_up_growth.py
   ```

2. To use with your own dataset:
   - Prepare a transaction dataset in the format of `example_transactions.txt`
   - Prepare a profit table in the format of `example_profit_table.txt`
   - Modify `run_up_growth.py` to point to your dataset files
   - Adjust the minimum utility threshold as needed

## Example Dataset Format

1. Transaction Dataset (`example_transactions.txt`):
   ```
   A:1 C:10 D:1
   A:2 C:6 E:2 G:5
   B:4 C:3 D:3 E:1
   ```
   Each line represents a transaction. Each item is in the format `item:quantity`.

2. Profit Table (`example_profit_table.txt`):
   ```
   A 5
   B 2
   C 1
   ```
   Each line contains an item and its profit value.

## References

Tseng, V. S., Shie, B.-E., Wu, C.-W., & Yu, P. S. (2013). Efficient algorithms for mining high utility itemsets from transactional databases. IEEE Transactions on Knowledge and Data Engineering, 25(8), 1772-1786.
