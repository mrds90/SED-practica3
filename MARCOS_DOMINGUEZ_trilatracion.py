import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Color cycle for plotting
CB_color_cycle = (
    "#377eb8",
    "#ff7f00",
    "#4daf4a",
    "#f781bf",
    "#a65628",
    "#984ea3",
    "#999999",
    "#e41a1c",
    "#dede00",
)

# Speed of sound in m/s
SOUND_SPEED = 340

def distance_from_time(t_ancla: np.ndarray, t_device: np.ndarray) -> np.ndarray:
    """
    Calculate the distance based on time difference.

    Parameters:
    t_ancla (np.ndarray): Reception times at anchors.
    t_device (np.ndarray): Transmission times from the device.

    Returns:
    np.ndarray: Calculated distances.
    """
    return (t_ancla - t_device) * SOUND_SPEED

def get_A_matrix(p_anclas_matrix: np.ndarray) -> np.ndarray:
    """
    Create the A matrix used in the trilateration algorithm.

    Parameters:
    p_anclas_matrix (np.ndarray): Anchor positions.

    Returns:
    np.ndarray: A matrix.
    """
    return p_anclas_matrix[1:] - p_anclas_matrix[0]

def get_b_matrix(p_ancla_matrix: np.ndarray, d_matrix: np.ndarray) -> np.ndarray:
    """
    Create the b matrix used in the trilateration algorithm.

    Parameters:
    p_ancla_matrix (np.ndarray): Anchor positions.
    d_matrix (np.ndarray): Distances calculated from time differences.

    Returns:
    np.ndarray: b matrix.
    """
    r_i1 = np.linalg.norm(p_ancla_matrix[0] - p_ancla_matrix[1:], axis=1)
    r_i1_matrix = np.tile(r_i1, (len(d_matrix), 1))
    b = ((d_matrix[:, 0]**2).reshape(-1, 1) - d_matrix[:, 1:]**2 + r_i1_matrix**2) / 2
    return b

def get_P_matrix(A: np.ndarray, b: np.ndarray, a1: np.ndarray) -> np.ndarray:
    """
    Solve for the position matrix P using least squares approximation.

    Parameters:
    A (np.ndarray): A matrix.
    b (np.ndarray): b matrix.
    a1 (np.ndarray): Reference position.

    Returns:
    np.ndarray: Estimated positions.
    """
    x = np.linalg.inv(A.T @ A) @ A.T @ b.T
    p = (x + a1).T
    return p

# Set current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Load data
t_device = pd.read_csv('data/tiempo_tx.csv', header=None).values
t_ancla = pd.read_csv('data/tiempo_rx.csv', header=None).values
p_ancla = pd.read_csv('data/anclas.csv', header=None).values
p_reference = pd.read_csv('data/posiciones.csv', header=None).values

# Calculate distances
d = distance_from_time(t_ancla, t_device)

# Calculate matrices for trilateration
A = get_A_matrix(p_ancla)
b = get_b_matrix(p_ancla, d)
a1 = p_ancla[0].reshape(-1, 1)

# Estimate positions
P = get_P_matrix(A, b, a1)

# Save estimated positions
np.savetxt("results/MARCOS_DOMINGUEZ_resultados.csv", P, delimiter=",", fmt='%f')

# Calculate errors
error_absoluto = np.abs(P - p_reference)
error_relativo = 100 * (error_absoluto) / p_reference

# Save relative errors
np.savetxt("results/MARCOS_DOMINGUEZ_ErrorRelativo.csv", error_relativo, delimiter=",", fmt='%f')

# Plotting
plt.figure(figsize=(15, 8))
plt.plot(P.T[0], P.T[1], label='Estimación', color=CB_color_cycle[0])
plt.plot(p_reference.T[0], p_reference.T[1], label='Posiciones', color=CB_color_cycle[1])
plt.scatter(p_ancla.T[0], p_ancla.T[1], linewidth=3, label='Anclas', color=CB_color_cycle[2])
plt.grid(which='major', linestyle='-', linewidth=0.5)
plt.grid(which='minor', linestyle='--', linewidth=0.5)
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.minorticks_on()
plt.legend()

# Save and show the plot
plt.savefig("results/MARCOS_DOMINGUEZ_figura.png")
plt.show()
