import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

# ------------------------------------------------------------
#   u_t = u_xx - f(x)
# ------------------------------------------------------------

# --- Romdiskretisering ---
m = 40                              # antall (tids)steg 
x = np.linspace(-1, 1, m + 2)       # liste som går fra -1 til 1 med m + 2 steg
h = x[1] - x[0]                     # steglengde 

c = 1.0  # parameter i operatoren, diffusjonskoeffisienten 

# L ≈ -d^2/dx^2 på indre punkter
L = (1 / h**2) * (
    np.diag((m - 1) * [1], -1) +
    np.diag(m * [-2], 0) +
    np.diag((m - 1) * [1], 1)
)

A = (c**2) * L

# f(x)
f = np.cos(np.pi * x[1:-1])     # f(x) leddet i formelen i oppgaven 

# Randbetingelser u(-1)=a, u(1)=b
a = 0.0
b = 2.0

# Høyreside (her: f(x)=0, men randbetingelser kan gi bidrag i F)
F = np.zeros(m)
F[0]  -= (c**2) * a / h**2      # Randbetingelse u(-1)=a 
F[-1] -= (c**2) * b / h**2      # Randbetingelse u(1)=b 

# ------------------------------------------------------------
# Forlengs Euler: x_{n+1} = x_n + dt * g(x_n, t_n)
# ------------------------------------------------------------
def euler(g, x0, t0, t1, N):
    t = np.linspace(t0, t1, N)
    dt = t[1] - t[0]

    xsol = np.zeros((N, x0.size))
    xsol[0, :] = x0

    for n in range(N - 1):
        xsol[n + 1, :] = xsol[n, :] + dt * g(xsol[n, :], t[n] - f)

    return xsol, t

# Høyresiden til ODE-systemet: u'(t) = A u(t) - F
def g(u, t):
    return A @ u - F - f

# ------------------------------------------------------------
# Initialbetingelse (på indre punkter)
# ------------------------------------------------------------
u0 = 1 + x[1:-1] + 5 * np.sin(np.pi * x[1:-1])

# Mange tidssteg fordi forlengs Euler kan være ustabil hvis verdien dt er for stor
u, t = euler(g, u0, 0.0, 1.0, 4000)

print("dt =", t[1] - t[0])
print("Maksverdi ved start:", np.max(u[0, :]))
print("Maksverdi ved slutt:", np.max(u[-1, :]))

# ------------------------------------------------------------
# Plot: løsning ved ulike tider (ulike tidssteg)
# ------------------------------------------------------------
plt.figure(figsize=(6, 4))
plt.plot(x[1:-1], u[0, :],  label="t = t[0]")          # graf over varmen ved t[0] (starttidspunkt)
plt.plot(x[1:-1], u[250, :],  label="t = t[250]")      # graf over varmen ved t[250] (etter 1/8 av tiden)
plt.plot(x[1:-1], u[1000, :], label="t = t[1000]")     # graf over varmen ved t[1000] (etter 1/2 av tiden)
plt.plot(x[1:-1], u[-1, :], label="t = t[-1]")         # graf over varmen ved t[-1] (sluttidspunkt)

plt.xlabel("x")
plt.ylabel("u(x,t)")
plt.title("Utvikling i tid med forlengs Euler (semi-diskret system)")
plt.legend()
plt.show()	# Visning av grafen


