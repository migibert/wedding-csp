# Wedding Seating Optimization

## Overview

This project optimizes wedding seating arrangements using Google OR-Tools and Constraint Programming (CP). It considers various constraints like affinities, anti-affinities, and table capacities to create an optimal seating arrangement.

## Features

- **Hard Constraints:** Ensures each guest is assigned to exactly one table and that table capacities are respected.
- **Soft Constraints:** Maximizes affinities and minimizes anti-affinities.
- **External JSON Dataset:** Makes it easy to modify guest lists, affinities, and table details.
- **Visualization:** Generates a seating chart for better understanding.
- **Docker Support:** Run the solver inside a container for easy deployment.

## Installation

### Local Setup

Ensure you have Python installed (>=3.9). Then, clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

### Docker Setup

To build and run the project inside a Docker container:

```bash
docker build -t wedding-seating .
docker run wedding-seating <path_to_dataset>.json
```

## Usage

### Running the Solver

To generate the optimal seating arrangement, run:

```bash
python solver.py <dataset>.json
```

### Expected Output

The script will return a JSON-like dictionary mapping guests to tables:

```json
{
  "Atlantic": ["Alice", "Bob", "Charlie", "Diana"],
  "Pacific": ["Eve", "Frank", "Grace", "Henry"],
  "Arctic": ["Isabel", "Jack", "Karen", "Liam"],
  "Antarctic": ["Mona", "Nathan", "Olivia", "Paul"]
}
```

## Dataset Format (`dataset.json`)

This JSON file defines the guests, affinities, and table capacities.

```json
{
  "guests": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Isabel", "Jack"],
  "affinities": {"Alice": {"Bob": 10, "Charlie": -3}},
  "tables": {"Atlantic": {"capacity": 5}, "Pacific": {"capacity": 5}}
}
```
