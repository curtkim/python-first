import ase
from ase.data import atomic_masses
from ase.units import fs
from ase.md.verlet import VelocityVerlet
import nnp.md as md
import sys
import math
import matplotlib.pyplot as plt

def gravity(chemical_symbols, coordinates, _cell, _pbc):
    assert len(chemical_symbols) == coordinates.shape[0]
    atomic_numbers = {'H': 0, 'C': 6}
    mass = coordinates.new_tensor(
        [atomic_masses[atomic_numbers[s]] for s in chemical_symbols])
    inv_r = 1 / coordinates.norm(dim=1)
    potential_energies = - mass * inv_r
    return potential_energies.sum()

calculator = md.Calculator(gravity)
planets = ase.Atoms('CH', [[1, 0, 0], [2, 0, 0]])

planets.set_velocities([[0, 1, 0], [0, 1 / math.sqrt(2), 0]])
planets.set_calculator(calculator)

X1 = []
Y1 = []
Z1 = []
X2 = []
Y2 = []
Z2 = []


def dump_positions():
    (x1, y1, z1), (x2, y2, z2) = planets.get_positions()
    X1.append(x1)
    Y1.append(y1)
    Z1.append(z1)
    X2.append(x2)
    Y2.append(y2)
    Z2.append(z2)


dyn = VelocityVerlet(planets, timestep=0.01 * fs)
dyn.attach(dump_positions)
dyn.run(20000)

if __name__ == '__main__':
    plt.clf()
    plt.plot(X1, Y1, label='C')
    plt.plot(X2, Y2, label='H')
    plt.legend()
    plt.axes().set_aspect('equal')
    plt.show()


