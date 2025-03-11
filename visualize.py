import json

import matplotlib.pyplot as plt


def visualize_seating(seating):
    fig, ax = plt.subplots()
    y_pos = range(len(seating))
    
    for i, (table, guests) in enumerate(seating.items()):
        ax.text(0.5, 1 - (i / len(seating)), f"{table}: {', '.join(guests)}",
                ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightblue', alpha=0.5))
    
    plt.axis("off")
    plt.title("Wedding Seating Arrangement")
    plt.show()

if __name__ == "__main__":
    with open("solution.json", "r") as file:
        seating = json.load(file)
    visualize_seating(seating)