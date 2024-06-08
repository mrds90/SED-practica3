import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

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

SOUND_SPEED = 340

def distance_from_time(t_ancla, t_device):
    return ((t_ancla - t_device) * SOUND_SPEED)

def get_A_matrix(p_anclas_matrix):
    return p_anclas_matrix[1:] - p_anclas_matrix[0]

def get_b_matrix(p_ancla_matrix, d_matrix):
    r_i1 = np.linalg.norm(p_ancla_matrix[0]- p_ancla_matrix[1:], axis=1)
    r_i1_matrix = np.tile(r_i1, (len(d_matrix), 1))
    b = ((d_matrix[:, 0]**2).reshape(-1, 1) -d_matrix[:, 1:]**2 + r_i1_matrix ** 2)/2
    return b

def get_P_matrix(A, b, a1):
    x = np.linalg.inv(A.T @ A) @ A.T @ b.T
    p = (x + a1).T
    return p
    
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

t_device = pd.read_csv('data/tiempo_tx.csv', header=None)
t_device = np.array(t_device.values)
t_ancla = pd.read_csv('data/tiempo_rx.csv', header=None)
t_ancla = np.array(t_ancla.values)
d = distance_from_time(t_ancla, t_device)

# print(d)
p_ancla = pd.read_csv('data/anclas.csv', header=None)
p_ancla = np.array(p_ancla.values)

A = get_A_matrix(p_ancla)

b = get_b_matrix(p_ancla, d)

a1 = p_ancla[0].reshape(-1, 1)

P = get_P_matrix(A, b, a1)

np.savetxt("results/MARCOS_DOMINGUEZ_resultados.csv", P, delimiter=",", fmt='%f')

p_reference = pd.read_csv('data/posiciones.csv', header=None)
p_reference = np.array(p_reference.values)

error_absoluto = np.abs(P-p_reference)
error_relativo = 100*(error_absoluto)/p_reference

np.savetxt("results/MARCOS_DOMINGUEZ_ErrorRelativo.csv", error_relativo, delimiter=",", fmt='%f')


plt.figure(figsize=(15, 8))
plt.plot(P.T[:][0], P.T[:][1], label='Estimación', color=CB_color_cycle[0])
plt.plot(p_reference.T[:][0], p_reference.T[:][1], label='Posiciones', color=CB_color_cycle[1])
plt.scatter(p_ancla.T[:][0], p_ancla.T[:][1], linewidth=3, label='Anclas', color=CB_color_cycle[2])
plt.grid(which='major', linestyle='-', linewidth=0.5)
plt.grid(which='minor', linestyle='--', linewidth=0.5)
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.minorticks_on()
plt.legend()

plt.savefig("results/MARCOS_DOMINGUEZ_figura.png")

plt.show()