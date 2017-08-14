# -*- coding: utf-8 -*-
# ***********************************************************************
#       Copyright (C) 2014 - 2017 Oscar Gerardo Lazo Arjona             *
#              <oscar.lazo@correo.nucleares.unam.mx>                    *
#                                                                       *
#  This file is part of FAST.                                           *
#                                                                       *
#  FAST is free software: you can redistribute it and/or modify         *
#  it under the terms of the GNU General Public License as published by *
#  the Free Software Foundation, either version 3 of the License, or    *
#  (at your option) any later version.                                  *
#                                                                       *
#  FAST is distributed in the hope that it will be useful,              *
#  but WITHOUT ANY WARRANTY; without even the implied warranty of       *
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
#  GNU General Public License for more details.                         *
#                                                                       *
#  You should have received a copy of the GNU General Public License    *
#  along with FAST.  If not, see <http://www.gnu.org/licenses/>.        *
#                                                                       *
# ***********************************************************************

r"""This module contains all the fast routines for optical Bloch equations.

Here is an example with rubidum 87.

>>> import fast
>>> element = "Rb"; isotope = 87; N = 5
>>> fine_states = [fast.State(element, isotope, N, 0, 1/fast.Integer(2)),
...                fast.State(element, isotope, N, 1, 3/fast.Integer(2))]

>>> magnetic_states = fast.make_list_of_states(fine_states, "magnetic")
>>> Ne = len(magnetic_states)
>>> Nl = 2
>>> E0 = [1e2, 1e2]
>>> epsilonp = [[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]

>>> omega, gamma, r = fast.calculate_matrices(magnetic_states)
>>> omega_level = [omega[i][0] for i in range(Ne)]
>>> r = fast.helicity_to_cartesian(r, numeric=True)
>>> rm = np.array([[[r[p, i, j]*fast.symbolic.delta_greater(i, j)*a0
...                for j in range(Ne)] for i in range(Ne)]
...                for p in range(3)])

>>> def coupled2(l, i, j):
...     if r[0, i, j] != 0 or \
...        r[1, i, j] != 0 or \
...        r[2, i, j] != 0:
...         if i < j:
...             i, j = j, i
...         if magnetic_states[j].f == 1 and l == 0:
...             return 1.0
...         if magnetic_states[j].f == 2 and l == 1:
...             return 1.0
...         else:
...             return 0.0
...     else:
...         return 0.0

>>> xi = np.array([[[coupled2(l, i, j)
...                for j in range(Ne)] for i in range(Ne)]
...                for l in range(Nl)])

>>> phase = phase_transformation(Ne, Nl, rm, xi, return_equations=False)
>>> detuning_knob = [fast.symbols("delta"+str(i+1)) for i in range(Nl)]
>>> hamiltonian = fast_hamiltonian(E0, epsilonp, detuning_knob, rm,
...                                omega_level, xi, phase)

>>> detuning_knob = [0.0, 0.0]
>>> print hamiltonian(detuning_knob)/hbar_num/2/np.pi*1e-6
[[   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    1.74562297+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    1.35215374+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
    -1.56133265+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    1.56133265+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   -1.74562297+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    1.35215374+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   72.22180189+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     1.56133265+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    1.56133265+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
    72.22180189+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j   -0.60470154+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.78066633+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    1.97494695+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j   72.22180189+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j   -0.69824919+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     2.09474757+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j   72.22180189+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   -0.60470154+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   -0.78066633+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    1.97494695+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   72.22180189+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
    -1.56133265+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    1.56133265+0.j    0.00000000+0.j]
 [   0.00000000+0.j   -1.56133265+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   1.74562297+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
    -0.60470154+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j   72.22180189+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j   -0.69824919+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j   72.22180189+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j   -1.74562297+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j   -0.60470154+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   72.22180189+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    1.56133265+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
   229.16195450+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   1.35215374+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.78066633+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j  229.16195450+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    1.56133265+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j  229.16195450+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    1.35215374+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j   -0.78066633+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j  229.16195450+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j   -1.56133265+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
   229.16195450+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    1.56133265+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     1.97494695+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    2.09474757+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    1.97494695+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    1.56133265+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]
 [   0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j
     0.00000000+0.j    0.00000000+0.j    0.00000000+0.j    0.00000000+0.j]]

"""

from sympy import Symbol, diff
from fast.symbolic import cartesian_dot_product, define_frequencies
from fast.symbolic import define_laser_variables
from scipy.constants import physical_constants

import numpy as np
import sympy

hbar_num = physical_constants["Planck constant over 2 pi"][0]
e_num = physical_constants["elementary charge"][0]
a0 = physical_constants["Bohr radius"][0]


def phase_transformation(Ne, Nl, rm, xi, return_equations=False):
    """Returns a phase transformation theta_i.

    The phase transformation is defined in a way such that
        theta1 + omega_level1 = 0.

    >>> xi = np.zeros((1, 2, 2))
    >>> xi[0, 1, 0] = 1.0
    >>> xi[0, 0, 1] = 1.0
    >>> rm = np.zeros((3, 2, 2))
    >>> rm[0, 1, 0] = 1.0
    >>> rm[1, 1, 0] = 1.0
    >>> rm[2, 1, 0] = 1.0
    >>> phase_transformation(2, 1, rm, xi)
    [-omega_1, -omega_1 - varpi_1]

    """
    # We first define the needed variables
    E0, omega_laser = define_laser_variables(Nl)
    theta = [Symbol('theta'+str(i+1)) for i in range(Ne)]

    # We check for the case of xi being a list of matrices.
    if type(xi) == list:
        xi = np.array([[[xi[l][i, j]
                       for j in range(Ne)] for i in range(Ne)]
                       for l in range(Nl)])

    # We find all the equations that the specified problem has to fulfil.
    eqs = []
    for i in range(Ne):
        for j in range(0, i):
            if (rm[0][i, j] != 0) or \
               (rm[1][i, j] != 0) or \
               (rm[2][i, j] != 0):
                for l in range(Nl):
                    if xi[l, i, j] == 1:
                        eqs += [-omega_laser[l] + theta[j] - theta[i]]

    if return_equations:
        return eqs

    # We solve the system of equations.
    # print eqs
    # print theta
    sol = sympy.solve(eqs, theta, dict=True)
    # print sol
    sol = sol[0]
    # We add any missing theta that may be left outside if the system is
    # under determined.

    extra_thetas = []
    for i in range(Ne):
        if theta[i] not in sol.keys():
            sol.update({theta[i]: theta[i]})
            extra_thetas += [theta[i]]

    # We make the solution such that theta1 + omega_level1 = 0.
    omega_level, omega, gamma = define_frequencies(Ne)
    eq_crit = sol[theta[0]] + omega_level[0]
    ss = sympy.solve(eq_crit, extra_thetas[0])[0]
    ss = {extra_thetas[0]: ss}

    sol_simple = [sol[theta[i]].subs(ss)
                  for i in range(Ne)]

    # sol = []
    # for i in range(Ne):
    #     soli = []
    #     for l in range(Nl):
    #         soli += [sympy.diff(sol_simple[theta[i]], omega_laser[l])]
    #     sol += [soli]

    return sol_simple


def define_simplification(omega_level, xi, Nl):
    """Return a simplifying function, its inverse, and simplified frequencies.

    This implements an index iu that labels energies in a non-degenerate
    way.

    >>> Ne = 6
    >>> Nl = 2
    >>> omega_level = [0.0, 100.0, 100.0, 200.0, 200.0, 300.0]
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    >>> aux = define_simplification(omega_level, xi, Nl)
    >>> u, invu, omega_levelu, Neu, xiu = aux
    >>> print omega_levelu
    [0.0, 100.0, 200.0, 300.0]
    >>> print Neu
    4
    >>> print xiu
    [[[ 0.  1.  0.  0.]
      [ 1.  0.  0.  0.]
      [ 0.  0.  0.  0.]
      [ 0.  0.  0.  0.]]
    <BLANKLINE>
     [[ 0.  0.  1.  1.]
      [ 0.  0.  0.  0.]
      [ 1.  0.  0.  0.]
      [ 1.  0.  0.  0.]]]

    """
    try:
        Ne = len(omega_level)
    except:
        Ne = omega_level.shape[0]
    #####################################
    # 1 We calculate the symplifying functions.
    om = omega_level[0]
    iu = 0; Neu = 1
    omega_levelu = [om]
    d = {}; di = {0: 0}
    for i in range(Ne):
        if omega_level[i] != om:
            iu += 1
            om = omega_level[i]
            Neu += 1
            omega_levelu += [om]
            di.update({iu: i})
        d.update({i: iu})

    def u(i):
        return d[i]

    def invu(iu):
        return di[iu]

    #####################################
    # 2 We build the simplified xi.
    Neu = len(omega_levelu)
    xiu = np.array([[[xi[l, invu(i), invu(j)]
                    for j in range(Neu)] for i in range(Neu)]
                    for l in range(Nl)])
    #####################################
    return u, invu, omega_levelu, Neu, xiu


def find_omega_min(omega_levelu, Neu, Nl, xiu):
    r"""Find the smallest transition frequency for each field.

    >>> Ne = 6
    >>> Nl = 2
    >>> omega_level = [0.0, 100.0, 100.0, 200.0, 200.0, 300.0]
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    >>> aux = define_simplification(omega_level, xi, Nl)
    >>> u, invu, omega_levelu, Neu, xiu = aux
    >>> find_omega_min(omega_levelu, Neu, Nl, xiu)
    ([100.0, 200.0], [1, 2], [0, 0])

    """
    omega_min = []; iu0 = []; ju0 = []
    for l in range(Nl):
        omegasl = []
        for iu in range(Neu):
            for ju in range(iu):
                if xiu[l, iu, ju] == 1:
                    omegasl += [(omega_levelu[iu]-omega_levelu[ju], iu, ju)]
        omegasl = list(sorted(omegasl))
        omega_min += [omegasl[0][0]]
        iu0 += [omegasl[0][1]]
        ju0 += [omegasl[0][2]]

    return omega_min, iu0, ju0


def detunings_indices(Neu, Nl, xiu):
    r"""Get the indices of the transitions of all fields.

    They are returned in the form
    [[(i1, j1), (i2, j2)], ...,[(i1, j1)]].
    that is, one list of pairs of indices for each field.

    >>> Ne = 6
    >>> Nl = 2
    >>> omega_level = [0.0, 100.0, 100.0, 200.0, 200.0, 300.0]
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    >>> aux = define_simplification(omega_level, xi, Nl)
    >>> u, invu, omega_levelu, Neu, xiu = aux
    >>> detunings_indices(Neu, Nl, xiu)
    [[(1, 0)], [(2, 0), (3, 0)]]

    """
    pairs = []
    for l in range(Nl):
        ind = []
        for iu in range(Neu):
            for ju in range(iu):
                if xiu[l, iu, ju] == 1:
                    ind += [(iu, ju)]
        pairs += [ind]
    return pairs


def detunings_code(Neu, Nl, pairs, omega_levelu, iu0, ju0):
    r"""Get the code to calculate the simplified detunings.

    >>> Ne = 6
    >>> Nl = 2
    >>> omega_level = [0.0, 100.0, 100.0, 200.0, 200.0, 300.0]
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    >>> aux = define_simplification(omega_level, xi, Nl)
    >>> u, invu, omega_levelu, Neu, xiu = aux
    >>> omega_min, iu0, ju0 = find_omega_min(omega_levelu, Neu, Nl, xiu)
    >>> pairs = detunings_indices(Neu, Nl, xiu)
    >>> print detunings_code(Neu, Nl, pairs, omega_levelu, iu0, ju0)
        delta1_2_1 = detuning_knob[0]
        delta2_3_1 = detuning_knob[1]
        delta2_4_1 = detuning_knob[1] + (-100.0)
    <BLANKLINE>

    """
    code_det = ""

    for l in range(Nl):
        for pair in pairs[l]:
            iu, ju = pair
            code_det += "    delta"+str(l+1)
            code_det += "_"+str(iu+1)
            code_det += "_"+str(ju+1)
            code_det += " = detuning_knob["+str(l)+"]"
            corr = -omega_levelu[iu]+omega_levelu[iu0[l]]
            corr = +omega_levelu[ju0[l]]-omega_levelu[ju] + corr
            if corr != 0:
                code_det += " + ("+str(corr)+")"
            code_det += "\n"
    return code_det


def detunings_combinations(pairs):
    r"""Return all combinations of detunings.

    >>> Ne = 6
    >>> Nl = 2
    >>> omega_level = [0.0, 100.0, 100.0, 200.0, 200.0, 300.0]
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    >>> aux = define_simplification(omega_level, xi, Nl)
    >>> u, invu, omega_levelu, Neu, xiu = aux
    >>> pairs = detunings_indices(Neu, Nl, xiu)
    >>> detunings_combinations(pairs)
    [[(1, 0), (2, 0)], [(1, 0), (3, 0)]]

    """
    def iter(pairs, combs, l):
        combs_n = []
        for i in range(len(combs)):
            for j in range(len(pairs[l])):
                combs_n += [combs[i] + [pairs[l][j]]]
        return combs_n

    Nl = len(pairs)
    combs = [[pairs[0][k]] for k in range(len(pairs[0]))]
    for l in range(1, Nl):
        combs = iter(pairs, combs, 1)

    return combs


def detunings_rewrite(expr, combs, omega_laser, symb_omega_levelu,
                      omega_levelu, iu0, ju0):
    r"""Rewrite a symbolic expression in terms of allowed transition detunings.

    >>> Ne = 6
    >>> Nl = 2
    >>> omega_level = [0.0, 100.0, 100.0, 200.0, 200.0, 300.0]
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    >>> aux = define_simplification(omega_level, xi, Nl)
    >>> u, invu, omega_levelu, Neu, xiu = aux
    >>> omega_min, iu0, ju0 = find_omega_min(omega_levelu, Neu, Nl, xiu)
    >>> pairs = detunings_indices(Neu, Nl, xiu)
    >>> combs = detunings_combinations(pairs)
    >>> symb_omega_levelu, omega, gamma = define_frequencies(Neu)
    >>> E0, omega_laser = define_laser_variables(Nl)

    Most times it is possible to express these combinations of optical
    frequencies in terms of allowed transition detunings.

    >>> expr = +(omega_laser[0]-(symb_omega_levelu[1]-symb_omega_levelu[0]))
    >>> expr += -(omega_laser[1]-(symb_omega_levelu[3]-symb_omega_levelu[0]))
    >>> expr
    -omega_2 + omega_4 + varpi_1 - varpi_2
    >>> detunings_rewrite(expr, combs, omega_laser, symb_omega_levelu,
    ...                   omega_levelu, iu0, ju0)
    '+delta1_2_1-delta2_4_1'

    But some times it is not possible:

    >>> expr = +(omega_laser[1]-(symb_omega_levelu[1]-symb_omega_levelu[0]))
    >>> expr += -(omega_laser[0]-(symb_omega_levelu[3]-symb_omega_levelu[0]))
    >>> expr
    -omega_2 + omega_4 - varpi_1 + varpi_2
    >>> detunings_rewrite(expr, combs, omega_laser, symb_omega_levelu,
    ...                   omega_levelu, iu0, ju0)
    '-detuning_knob[0]+detuning_knob[1]'

    """
    Nl = len(omega_laser)
    Neu = len(symb_omega_levelu)
    # We find the coefficients a_i of the field frequencies.
    a = [diff(expr, omega_laser[l]) for l in range(Nl)]

    # We look for a combination of the detunings obtained with the
    # function detunings_code. For each combination we sum the
    # detunings weighed by a_i.
    success = False
    for comb in combs:
        expr_try = 0
        for l in range(Nl):
            expr_try += a[l]*(omega_laser[l] -
                              symb_omega_levelu[comb[l][0]] +
                              symb_omega_levelu[comb[l][1]])
        if expr-expr_try == 0:
            success = True
            break

    assign = ""
    if success:
        for l in range(Nl):
            if a[l] != 0:
                if a[l] == 1:
                    assign += "+"
                elif a[l] == -1:
                    assign += "-"
                assign += "delta"+str(l+1)
                assign += "_"+str(comb[l][0]+1)
                assign += "_"+str(comb[l][1]+1)
    else:
        # We get the code for Hii using detuning knobs.
        # We find out the remainder terms.
        _remainder = expr - sum([a[l]*omega_laser[l]
                                 for l in range(Nl)])
        # We find the coefficients of the remainder.
        b = [diff(_remainder, symb_omega_levelu[j]) for j in range(Neu)]
        # We calculate the remainder numerically.
        remainder = sum([b[j]*omega_levelu[j] for j in range(Neu)])
        # We add the contributions from the detuning knobs.
        remainder += sum([a[l]*(omega_levelu[iu0[l]] -
                                omega_levelu[ju0[l]])
                          for l in range(Nl)])
        # We get the code for Hii using detuning knobs.
        for l in range(Nl):
            if a[l] != 0:
                if a[l] == 1:
                    assign += "+"
                elif a[l] == -1:
                    assign += "-"
                assign += "detuning_knob["+str(l)+"]"
    return assign


def fast_hamiltonian(Ep, epsilonp, detuning_knob, rm, omega_level, xi, theta,
                     file_name=None):
    r"""Return a fast function that returns a Hamiltonian as a numerical array.

    INPUT:

    -  ``Ep`` - A list with the electric field amplitudes (real or complex).
    -  ``epsilonp`` - A list of the polarization vectors of the fields \
    (real or complex).
    -  ``detuning_knob`` - A list of the detunings of each field (relative \
    to the transition of lowest energy).
    -  ``rm`` -     The below-diagonal components
        of the position operator in the cartesian basis:

        .. math::
            \vec{r}^{(-)}_{i j} = [ x_{ij}, y_{ij}, z_{ij} ]
            \hspace{1cm} \forall \hspace{1cm} 0 < j < i
    -  ``omega_level`` - The angular frequencies of each state.
    -  ``xi`` - An array whose ``xi[l, i, j]`` element is 1 if the \
     transition :math:`|i\rangle \rightarrow |j\rangle`\ is driven by field \
     ``l`` and 0 otherwise.
    -  ``theta`` - A list of symbolic expressions representing a phase \
    transformation.
    -  ``file_name`` - A string indicating a file to save the function's \
    code.

    If the arguments Ep, epsilonp, and detuning_knob are symbolic amounts, \
    the returned function will accept numeric values of Ep, epsilonp, and \
    detuning_knob as arguments.

    All quantities should be in SI units.

    EXAMPLES:

    We build an example using states coupled like this:

     --- |4>        --- |5>          --- |6>
      ^              ^                ^
      |              |                |
      |    --- |2>   |     --- |3>    |
    2 |     ^      2 |      ^         | 2
      |   1 |        |    1 |         |
      |     |        |      |         |
    ------------------------------------- |1>

    With the numbers on kets labeling states and the plain numbers labeling
    fields.

    The number of states and fields:
    >>> Ne = 6
    >>> Nl = 2

    We invent some energy levels:
    >>> omega_level = np.array([0.0, 100.0, 100.0, 200.0, 200.0, 300.0])
    >>> omega_level = omega_level*1e6*2*np.pi

    We build the symbol xi, that chooses which laser couples which
    transition.
    >>> xi = np.zeros((Nl, Ne, Ne))
    >>> coup = [[(1, 0), (2, 0)], [(3, 0), (4, 0), (5, 0)]]
    >>> for l in range(Nl):
    ...     for pair in coup[l]:
    ...         xi[l, pair[0], pair[1]] = 1.0
    ...         xi[l, pair[1], pair[0]] = 1.0

    We invent some electric dipole matrix elements:
    >>> from scipy.constants import physical_constants
    >>> a0 = physical_constants["Bohr radius"][0]
    >>> rm = np.zeros((3, Ne, Ne))
    >>> for l in range(Nl):
    ...     for i in range(Ne):
    ...         for j in range(i):
    ...             if xi[l, i, j] != 0:
    ...                 rm[2, i, j] = float(i)*a0

    The phase transformation:
    >>> theta = phase_transformation(Ne, Nl, rm, xi)

    We define the possible arguments:
    >>> from sympy import symbols, pi
    >>> from fast.symbolic import polarization_vector
    >>> detuning_knob = symbols("delta1 delta2")
    >>> detuning_knob_vals = np.array([-1.0, 3.0])*1e6*2*np.pi

    >>> Ep, omega_laser = define_laser_variables(Nl)
    >>> Ep_vals = [1e2, 1e2]

    >>> alpha = symbols("alpha")
    >>> epsilon = polarization_vector(0, pi/2, alpha, 0, 1)
    >>> epsilonp = [epsilon, epsilon]
    >>> epsilonp_vals = [[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]

    There are 8 ways to call fast_hamiltonian:

    1 .- Get a function of detunings, field amplitudes, polarizations:
    >>> H1 = fast_hamiltonian(Ep, epsilonp, detuning_knob, rm,
    ...                       omega_level, xi, theta)

    2 .- Get a function of field amplitudes, polarizations:
    >>> H2 = fast_hamiltonian(Ep, epsilonp, detuning_knob_vals, rm,
    ...                       omega_level, xi, theta)

    3 .- Get a function of detunings, polarizations:
    >>> H3 = fast_hamiltonian(Ep_vals, epsilonp, detuning_knob, rm,
    ...                       omega_level, xi, theta)

    4 .- Get a function of detunings, field amplitudes:
    >>> H4 = fast_hamiltonian(Ep, epsilonp_vals, detuning_knob, rm,
    ...                       omega_level, xi, theta)

    5 .- Get a function of detunings:
    >>> H5 = fast_hamiltonian(Ep_vals, epsilonp_vals, detuning_knob, rm,
    ...                       omega_level, xi, theta)

    6 .- Get a function of field amplitudes:
    >>> H6 = fast_hamiltonian(Ep, epsilonp_vals, detuning_knob_vals, rm,
    ...                       omega_level, xi, theta)

    7 .- Get a function of polarizations:
    >>> H7 = fast_hamiltonian(Ep_vals, epsilonp, detuning_knob_vals, rm,
    ...                       omega_level, xi, theta)

    8 .- Get a function of nothing:
    >>> H8 = fast_hamiltonian(Ep_vals, epsilonp_vals, detuning_knob_vals, rm,
    ...                       omega_level, xi, theta)


    We test all of these combinations.
    >>> print H1(Ep_vals, epsilonp_vals, detuning_knob_vals) \
    ...     /hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H2(Ep_vals, epsilonp_vals)/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H3(epsilonp_vals, detuning_knob_vals)/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H4(Ep_vals, detuning_knob_vals)/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H5(detuning_knob_vals)/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H6(Ep_vals)/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H7(epsilonp_vals)/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    >>> print H8()/hbar_num/2/np.pi*1e-6
    [[  0.00000000+0.j   0.63977241+0.j   1.27954481+0.j   1.91931722+0.j
        2.55908963+0.j   3.19886203+0.j]
     [  0.63977241+0.j   1.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.27954481+0.j   0.00000000+0.j   1.00000000+0.j   0.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  1.91931722+0.j   0.00000000+0.j   0.00000000+0.j  -3.00000000+0.j
        0.00000000+0.j   0.00000000+0.j]
     [  2.55908963+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
       -3.00000000+0.j   0.00000000+0.j]
     [  3.19886203+0.j   0.00000000+0.j   0.00000000+0.j   0.00000000+0.j
        0.00000000+0.j  97.00000000+0.j]]

    """
    # We find out the number of fields and states.
    if True:
        Nl = len(Ep)
        Ne = np.array(rm[0]).shape[0]
        # We determine which arguments are constants.
        try:
            Ep = np.array([complex(Ep[l]) for l in range(Nl)])
            variable_Ep = False
        except:
            variable_Ep = True

        try:
            epsilonp = [np.array([complex(epsilonp[l][i]) for i in range(3)])
                        for l in range(Nl)]
            variable_epsilonp = False
        except:
            variable_epsilonp = True

        try:
            detuning_knob = np.array([float(detuning_knob[l])
                                      for l in range(Nl)])
            variable_detuning_knob = False
        except:
            variable_detuning_knob = True

        # We convert rm to a numpy array
        rm = np.array([[[complex(rm[k][i, j])
                       for j in range(Ne)] for i in range(Ne)]
                       for k in range(3)])
    # We establish the arguments of the output function.
    if True:
        code = ""
        code += "def hamiltonian("
        if variable_Ep: code += "Ep, "
        if variable_epsilonp: code += "epsilonp, "
        if variable_detuning_knob: code += "detuning_knob, "
        if code[-2:] == ", ":
            code = code[:-2]
        code += "):\n"

        code += '    r"""A fast calculation of the hamiltonian."""\n'
        code += "    H = np.zeros(("+str(Ne)+", "+str(Ne)+"), complex)\n\n"
    # We get the code for the below-diagonal elements.
    if True:
        code += "    # We calculate the below-diagonal elements.\n"
        for i in range(Ne):
            for j in range(i):
                for l in range(Nl):
                    if xi[l, i, j] == 1.0:
                        # We get the below-diagonal terms.
                        code += "    H["+str(i)+", "+str(j)+"] = "
                        # We get the code for Ep.
                        if variable_Ep:
                            code += "0.5*Ep["+str(l)+"]"

                        else:
                            code += str(0.5*Ep[l])
                        # We get the code for epsilonp dot rm
                        rmij = rm[:, i, j]
                        if variable_epsilonp:
                            code += "*cartesian_dot_product("
                            code += "epsilonp["+str(l)+"],"
                            code += str(list(rmij*e_num))+" )"
                        else:
                            dp = cartesian_dot_product(epsilonp[l], rmij)
                            dp = dp*e_num
                            code += "*("+str(dp)+")"

                        code += "\n"
    # We get the code for the above-diagonal elements.
    if True:
        code += "\n"
        code += """    # We calculate the above-diagonal elements.\n"""
        code += """    for i in range("""+str(Ne)+"""):\n"""
        code += """        for j in range(i+1, """+str(Ne)+"""):\n"""
        code += """            H[i, j] = H[j, i].conjugate()\n\n"""
    # We get the code for the diagonal elements.
    if True:
        code += "    # We calculate the diagonal elements.\n"
        # 1 We build the degeneration simplification and its inverse (to avoid
        # large combinatorics).
        aux = define_simplification(omega_level, xi, Nl)
        u, invu, omega_levelu, Neu, xiu = aux
        # For each field we find the smallest transition frequency, and its
        # simplified indices.
        omega_min, iu0, ju0 = find_omega_min(omega_levelu, Neu, Nl, xiu)
        # We get the code to calculate the non degenerate detunings.
        pairs = detunings_indices(Neu, Nl, xiu)
        if not variable_detuning_knob:
            code += "    detuning_knob = np.zeros("+str(Nl)+")\n"
            for l in range(Nl):
                code += "    detuning_knob["+str(l)+"] = " +\
                    str(detuning_knob[l])+"\n"

        code_det = detunings_code(Neu, Nl, pairs, omega_levelu, iu0, ju0)
        code += code_det

        code += "\n"
        #####################################
        # We find the coefficients a_l that multiply omega_laser_l in
        # H_ii = omega_level_iu + theta_iu = \sum_i a_i varpi_i + remainder
        _omega_level, omega, gamma = define_frequencies(Ne)
        _omega_levelu, omega, gamma = define_frequencies(Neu)
        E0, omega_laser = define_laser_variables(Nl)
        # So we build all combinations.
        combs = detunings_combinations(pairs)
        for i in range(Ne):
            _Hii = theta[i] + _omega_levelu[u(i)]
            assign = detunings_rewrite(_Hii, combs, omega_laser,
                                       _omega_levelu, omega_levelu,
                                       iu0, ju0)

            if assign != "":
                code += "    H["+str(i)+", "+str(i)+"] = "+assign+"\n"

    code += "\n"
    code += """    for i in range("""+str(Ne)+"""):\n"""
    code += """        H[i, i] = H[i, i]*"""+str(hbar_num)+"\n"

    code += "    return H\n"

    if file_name is not None:
        f = file(file_name, "w")
        f.write(code)
        f.close()

    hamiltonian = code
    # print code
    exec hamiltonian
    return hamiltonian


def vectorization(Ne, Nv=1, real=False, lower_triangular=True,
                  normalized=False):
    r"""Return functions to map matrix element indices to vectorized indices.

    This function returns a function Mu that takes a pair of indices i, j
    spanning Ne states, and returns an index mu spanning the elements of the
    vectorized density matrix. If complex=True.

    >>> def test_vectorization(Ne, Nv, real=False,
    ...                        lower_triangular=True, normalized=False):
    ...
    ...     Mu, IJ = vectorization(Ne, Nv, real, lower_triangular, normalized)
    ...     if normalized:
    ...         j0 = 1
    ...     else:
    ...         j0 = 0
    ...     for k in range(Nv):
    ...         for j in range(j0, Ne):
    ...             if real:
    ...                 muu = Mu(1, j, j, k)
    ...                 ss, ii, jj, kk = IJ(muu)
    ...                 print j, j, muu, j-ii, j-jj, k-kk, 1-ss
    ...             else:
    ...                 muu = Mu(j, j, k)
    ...                 ii, jj, kk = IJ(muu)
    ...                 print j, j, muu, j-ii, j-jj, k-kk
    ...         for j in range(Ne):
    ...             for i in range(j+1, Ne):
    ...                 if real:
    ...                     muu = Mu(1, i, j, k)
    ...                     ss, ii, jj, kk = IJ(muu)
    ...                     print i, j, muu, i-ii, j-jj, k-kk, 1-ss
    ...                     muu = Mu(-1, i, j, k)
    ...                     ss, ii, jj, kk = IJ(muu)
    ...                     print i, j, muu, i-ii, j-jj, k-kk, -1-ss
    ...                 else:
    ...                     muu = Mu(i, j, k)
    ...                     ii, jj, kk = IJ(muu)
    ...                     print i, j, muu, i-ii, j-jj, k-kk
    ...                 if not lower_triangular:
    ...                     if real:
    ...                         muu = Mu(1, j, i, k)
    ...                         ss, ii, jj, kk = IJ(muu)
    ...                         print j, i, muu, j-ii, i-jj, k-kk, 1-ss
    ...                         muu = Mu(-1, j, i, k)
    ...                         ss, ii, jj, kk = IJ(muu)
    ...                         print j, i, muu, j-ii, i-jj, k-kk, -1-ss
    ...                     else:
    ...                         muu = Mu(j, i, k)
    ...                         ii, jj, kk = IJ(muu)
    ...                         print i, j, muu, j-ii, i-jj, k-kk
    ...

    >>> Ne = 3
    >>> Nv = 3

    >>> test_vectorization(Ne, Nv, False, False, False)
    0 0 0 0 0 0
    1 1 1 0 0 0
    2 2 2 0 0 0
    1 0 3 0 0 0
    1 0 4 0 0 0
    2 0 5 0 0 0
    2 0 6 0 0 0
    2 1 7 0 0 0
    2 1 8 0 0 0
    0 0 9 0 0 0
    1 1 10 0 0 0
    2 2 11 0 0 0
    1 0 12 0 0 0
    1 0 13 0 0 0
    2 0 14 0 0 0
    2 0 15 0 0 0
    2 1 16 0 0 0
    2 1 17 0 0 0
    0 0 18 0 0 0
    1 1 19 0 0 0
    2 2 20 0 0 0
    1 0 21 0 0 0
    1 0 22 0 0 0
    2 0 23 0 0 0
    2 0 24 0 0 0
    2 1 25 0 0 0
    2 1 26 0 0 0


    >>> test_vectorization(Ne, Nv, False, False, True)
    1 1 0 0 0 0
    2 2 1 0 0 0
    1 0 2 0 0 0
    1 0 3 0 0 0
    2 0 4 0 0 0
    2 0 5 0 0 0
    2 1 6 0 0 0
    2 1 7 0 0 0
    1 1 8 0 0 0
    2 2 9 0 0 0
    1 0 10 0 0 0
    1 0 11 0 0 0
    2 0 12 0 0 0
    2 0 13 0 0 0
    2 1 14 0 0 0
    2 1 15 0 0 0
    1 1 16 0 0 0
    2 2 17 0 0 0
    1 0 18 0 0 0
    1 0 19 0 0 0
    2 0 20 0 0 0
    2 0 21 0 0 0
    2 1 22 0 0 0
    2 1 23 0 0 0

    >>> test_vectorization(Ne, Nv, False, True, False)
    0 0 0 0 0 0
    1 1 1 0 0 0
    2 2 2 0 0 0
    1 0 3 0 0 0
    2 0 4 0 0 0
    2 1 5 0 0 0
    0 0 6 0 0 0
    1 1 7 0 0 0
    2 2 8 0 0 0
    1 0 9 0 0 0
    2 0 10 0 0 0
    2 1 11 0 0 0
    0 0 12 0 0 0
    1 1 13 0 0 0
    2 2 14 0 0 0
    1 0 15 0 0 0
    2 0 16 0 0 0
    2 1 17 0 0 0

    >>> test_vectorization(Ne, Nv, False, True, True)
    1 1 0 0 0 0
    2 2 1 0 0 0
    1 0 2 0 0 0
    2 0 3 0 0 0
    2 1 4 0 0 0
    1 1 5 0 0 0
    2 2 6 0 0 0
    1 0 7 0 0 0
    2 0 8 0 0 0
    2 1 9 0 0 0
    1 1 10 0 0 0
    2 2 11 0 0 0
    1 0 12 0 0 0
    2 0 13 0 0 0
    2 1 14 0 0 0

    >>> test_vectorization(Ne, Nv, True, False, False)
    0 0 0 0 0 0 0
    1 1 1 0 0 0 0
    2 2 2 0 0 0 0
    1 0 3 0 0 0 0
    1 0 4 0 0 0 0
    0 1 5 0 0 0 0
    0 1 6 0 0 0 0
    2 0 7 0 0 0 0
    2 0 8 0 0 0 0
    0 2 9 0 0 0 0
    0 2 10 0 0 0 0
    2 1 11 0 0 0 0
    2 1 12 0 0 0 0
    1 2 13 0 0 0 0
    1 2 14 0 0 0 0
    0 0 15 0 0 0 0
    1 1 16 0 0 0 0
    2 2 17 0 0 0 0
    1 0 18 0 0 0 0
    1 0 19 0 0 0 0
    0 1 20 0 0 0 0
    0 1 21 0 0 0 0
    2 0 22 0 0 0 0
    2 0 23 0 0 0 0
    0 2 24 0 0 0 0
    0 2 25 0 0 0 0
    2 1 26 0 0 0 0
    2 1 27 0 0 0 0
    1 2 28 0 0 0 0
    1 2 29 0 0 0 0
    0 0 30 0 0 0 0
    1 1 31 0 0 0 0
    2 2 32 0 0 0 0
    1 0 33 0 0 0 0
    1 0 34 0 0 0 0
    0 1 35 0 0 0 0
    0 1 36 0 0 0 0
    2 0 37 0 0 0 0
    2 0 38 0 0 0 0
    0 2 39 0 0 0 0
    0 2 40 0 0 0 0
    2 1 41 0 0 0 0
    2 1 42 0 0 0 0
    1 2 43 0 0 0 0
    1 2 44 0 0 0 0

    >>> test_vectorization(Ne, Nv, True, False, True)
    1 1 0 0 0 0 0
    2 2 1 0 0 0 0
    1 0 2 0 0 0 0
    1 0 3 0 0 0 0
    0 1 4 0 0 0 0
    0 1 5 0 0 0 0
    2 0 6 0 0 0 0
    2 0 7 0 0 0 0
    0 2 8 0 0 0 0
    0 2 9 0 0 0 0
    2 1 10 0 0 0 0
    2 1 11 0 0 0 0
    1 2 12 0 0 0 0
    1 2 13 0 0 0 0
    1 1 14 0 0 0 0
    2 2 15 0 0 0 0
    1 0 16 0 0 0 0
    1 0 17 0 0 0 0
    0 1 18 0 0 0 0
    0 1 19 0 0 0 0
    2 0 20 0 0 0 0
    2 0 21 0 0 0 0
    0 2 22 0 0 0 0
    0 2 23 0 0 0 0
    2 1 24 0 0 0 0
    2 1 25 0 0 0 0
    1 2 26 0 0 0 0
    1 2 27 0 0 0 0
    1 1 28 0 0 0 0
    2 2 29 0 0 0 0
    1 0 30 0 0 0 0
    1 0 31 0 0 0 0
    0 1 32 0 0 0 0
    0 1 33 0 0 0 0
    2 0 34 0 0 0 0
    2 0 35 0 0 0 0
    0 2 36 0 0 0 0
    0 2 37 0 0 0 0
    2 1 38 0 0 0 0
    2 1 39 0 0 0 0
    1 2 40 0 0 0 0
    1 2 41 0 0 0 0

    >>> test_vectorization(Ne, Nv, True, True, False)
    0 0 0 0 0 0 0
    1 1 1 0 0 0 0
    2 2 2 0 0 0 0
    1 0 3 0 0 0 0
    1 0 4 0 0 0 0
    2 0 5 0 0 0 0
    2 0 6 0 0 0 0
    2 1 7 0 0 0 0
    2 1 8 0 0 0 0
    0 0 9 0 0 0 0
    1 1 10 0 0 0 0
    2 2 11 0 0 0 0
    1 0 12 0 0 0 0
    1 0 13 0 0 0 0
    2 0 14 0 0 0 0
    2 0 15 0 0 0 0
    2 1 16 0 0 0 0
    2 1 17 0 0 0 0
    0 0 18 0 0 0 0
    1 1 19 0 0 0 0
    2 2 20 0 0 0 0
    1 0 21 0 0 0 0
    1 0 22 0 0 0 0
    2 0 23 0 0 0 0
    2 0 24 0 0 0 0
    2 1 25 0 0 0 0
    2 1 26 0 0 0 0

    >>> test_vectorization(Ne, Nv, True, True, True)
    1 1 0 0 0 0 0
    2 2 1 0 0 0 0
    1 0 2 0 0 0 0
    1 0 3 0 0 0 0
    2 0 4 0 0 0 0
    2 0 5 0 0 0 0
    2 1 6 0 0 0 0
    2 1 7 0 0 0 0
    1 1 8 0 0 0 0
    2 2 9 0 0 0 0
    1 0 10 0 0 0 0
    1 0 11 0 0 0 0
    2 0 12 0 0 0 0
    2 0 13 0 0 0 0
    2 1 14 0 0 0 0
    2 1 15 0 0 0 0
    1 1 16 0 0 0 0
    2 2 17 0 0 0 0
    1 0 18 0 0 0 0
    1 0 19 0 0 0 0
    2 0 20 0 0 0 0
    2 0 21 0 0 0 0
    2 1 22 0 0 0 0
    2 1 23 0 0 0 0

    """
    real_map = {}; real_map_inv = {}
    comp_map = {}; comp_map_inv = {}
    mu_real = 0
    mu_comp = 0
    # We repeat the same thing for each velocity group.
    for k in range(Nv):
        # We get the mappings of populations.
        if normalized:
            start = 1
        else:
            start = 0
        for i in range(start, Ne):
            comp_map.update({(i, i, k): mu_comp})
            comp_map_inv.update({mu_comp: (i, i, k)})
            mu_comp += 1
            real_map.update({(1, i, i, k): mu_real})
            real_map_inv.update({mu_real: (1, i, i, k)})
            mu_real += 1

        # We get the mappings for coherences.
        for j in range(Ne):
            for i in range(j+1, Ne):
                comp_map.update({(i, j, k): mu_comp})
                comp_map_inv.update({mu_comp: (i, j, k)})
                mu_comp += 1
                for s in [1, -1]:
                    real_map.update({(s, i, j, k): mu_real})
                    real_map_inv.update({mu_real: (s, i, j, k)})
                    mu_real += 1

                if not lower_triangular:
                    comp_map.update({(j, i, k): mu_comp})
                    comp_map_inv.update({mu_comp: (j, i, k)})
                    mu_comp += 1
                    for s in [1, -1]:
                        real_map.update({(s, j, i, k): mu_real})
                        real_map_inv.update({mu_real: (s, j, i, k)})
                        mu_real += 1

        # if normalized:
        #     three.pop((0, 0))
        #     four.pop((0, 0, 1))
        #
        #     three_inv.pop(0)
        #     four_inv.pop(0)

    def Mu_comp(i, j, k=0):
        return comp_map[(i, j, k)]

    def Mu_real(s, i, j, k=0):
        return real_map[(s, i, j, k)]

    def IJ_comp(mu):
        return comp_map_inv[mu]

    def IJ_real(mu):
        return real_map_inv[mu]

    if real:
        return Mu_real, IJ_real
    else:
        return Mu_comp, IJ_comp


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
