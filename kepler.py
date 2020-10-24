# Ejercicio basado en https://docs.sympy.org/latest/modules/physics/units/examples.html#equation-with-quantities
# Sobre Kepler https://en.wikipedia.org/wiki/Johannes_Kepler

from sympy import solve, symbols, pi, Eq  # Cargamos objetos directos de Sympy
# Unidades S.I.
from sympy.physics.units import meter, kilogram, second, kelvin, newton, day, year
# Cargamos la función convert_to para pasar de unas unidades a otras
from sympy.physics.units import convert_to
# Cargamos constantes
# La constante de gravitación universal https://www.google.com/search?q=gravitational+constant
from sympy.physics.units import gravitational_constant as G
from sympy.physics.units import speed_of_light as c

T = symbols("T")  # Incógnita: periodo de giro (T)
a = 108208000e3*meter  # Dato conocido: semieje mayor de Venus
M0 = 1.9891e30*kilogram  # Dato conocido: masa del Sol

eq_kepler = Eq(T**2 / a**3, 4*pi**2 / G / M0)  # Ecuación de Kepler
# Despejamos T, el resultado acaba en otra variable llamada "solution"
solution = solve(eq_kepler, T)[1]

# print(solution)
print(convert_to(solution, [year]).n())

# Conversión entre unidades https://docs.sympy.org/latest/modules/physics/units/quantities.html
#print(convert_to(G, [newton, meter,  kilogram]))
