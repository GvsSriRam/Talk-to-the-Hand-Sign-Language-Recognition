import numpy as np

def get_relative_positions(x):
    relative_positions = []
    for i in range(1, len(x)):
        relative_positions.append(x[i] - x[0])
    return np.array(relative_positions)
