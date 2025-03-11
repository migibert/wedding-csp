import argparse
import json

import matplotlib.pyplot as plt
import numpy as np
from ortools.sat.python import cp_model


def load_data(dataset_path):
    with open(dataset_path, "r") as file:
        return json.load(file)

def solve_seating(dataset_path):
    data = load_data(dataset_path)
    guests = data["guests"]
    tables = list(data["tables"].keys())
    capacities = {t: data["tables"][t]["capacity"] for t in tables}
    affinities = data.get("affinities", {})
    
    model = cp_model.CpModel()
    assignment = {}
    
    for g in guests:
        for t in tables:
            assignment[(g, t)] = model.NewBoolVar(f"guest_{g}_table_{t}")
    
    for g in guests:
        model.Add(sum(assignment[(g, t)] for t in tables) == 1)
    
    for t in tables:
        model.Add(sum(assignment[(g, t)] for g in guests) <= capacities[t])
    
    affinity_terms = []
    for g1 in guests:
        for g2 in guests:
            if g1 in affinities and g2 in affinities[g1]:
                for t in tables:
                    pair_var = model.NewBoolVar(f"pair_{g1}_{g2}_at_{t}")
                    model.Add(pair_var <= assignment[(g1, t)])
                    model.Add(pair_var <= assignment[(g2, t)])
                    affinity_terms.append(pair_var * affinities[g1][g2])
    
    model.Maximize(sum(affinity_terms))
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        seating = {t: [] for t in tables}
        for g in guests:
            for t in tables:
                if solver.Value(assignment[(g, t)]):
                    seating[t].append(g)
        return seating
    else:
        return "No solution found"

def visualize_seating(seating):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    table_radius = 0.5
    seat_radius = 0.08
    num_tables = len(seating)
    
    for i, (table, guests) in enumerate(seating.items()):
        angle_offset = (2 * np.pi / num_tables) * i
        table_x = np.cos(angle_offset) * 1.2
        table_y = np.sin(angle_offset) * 1.2
        ax.add_patch(plt.Circle((table_x, table_y), table_radius, color='lightblue', alpha=0.6))
        ax.text(table_x, table_y, table, ha='center', va='center', fontsize=14, fontweight='bold')
        
        num_seats = max(8, len(guests))
        angle_step = 2 * np.pi / num_seats
        for j, guest in enumerate(guests):
            seat_x = table_x + np.cos(angle_step * j) * (table_radius + seat_radius * 2)
            seat_y = table_y + np.sin(angle_step * j) * (table_radius + seat_radius * 2)
            ax.add_patch(plt.Circle((seat_x, seat_y), seat_radius, color='lightcoral', alpha=0.8))
            ax.text(seat_x, seat_y, guest, ha='center', va='center', fontsize=10)
    
    plt.title("Wedding Seating Arrangement", fontsize=16, fontweight='bold')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Wedding Seating Arrangement")
    parser.add_argument("dataset", help="Dataset path", type=str, default="dataset/default.json")
    args = parser.parse_args()
    print(args.dataset)
    result = solve_seating(args.dataset)
    print(result)
    visualize_seating(result)

    import argparse

