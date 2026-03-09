import numpy as np
import matplotlib.pyplot as plt

# Antall punkter (inkludert randpunkter)
N = 50
h = 2/N  # steglengde

# Lag grid på [-1,1]
x = np.linspace(-1, 1, N+1)

# Analytisk løsning
u_eksakt = -(1/np.pi**2)*np.cos(np.pi*x) + (1 - 1/np.pi**2)*x + 1

# Sett opp tridiagonal matrise A
A = -2*np.eye(N-1) + np.eye(N-1, k=1) + np.eye(N-1, k=-1)

# Høyreside b
b = h**2 * np.cos(np.pi*x[1:N])

# Juster for randbetingelser
b[0] = b[0] - 0    # u(-1) = 0
b[-1] = b[-1] - 2   # u(1) = 2

# Løs det lineære systemet
u_innere = np.linalg.solve(A, b)

# Sett sammen den komplette løsningen inkl. randpunkter
u_numerisk = np.zeros(N+1)
u_numerisk[0] = 0      # u(-1)
u_numerisk[N] = 2      # u(1)
u_numerisk[1:N] = u_innere

# Tegn graf
plt.plot(x, u_eksakt, label="Analytisk løsning")
plt.plot(x, u_numerisk, '--', label="Numerisk løsning")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.title("Sammenligning av analytisk og numerisk løsning")
plt.legend()
plt.show()
