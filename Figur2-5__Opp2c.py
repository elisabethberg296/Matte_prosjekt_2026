import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# parametere (fra oppgave 2b)
v_max = 22.2  # m/s (80 km/t)
u_max = 0.2   # biler/meter (5m per bil)
L = 1000      # strekningen [-1000, 1000]
p_values = [1, 2, 5]

dx = 10                     # vstand mellom punkter (h)
x = np.arange(-L, L + dx, dx)
# dt var 0.4 på figur 2-4, og ble byttet til 0.1 til figur 5
dt = 0.4                   # tidssteg (k) - må overholde dt <= dx/v_max
t_slutt = 60                # simuleringstid i sekunder

# fluks funksjonen J
def flux(u, p):
    # J(u) = u * v(u)
    return u * v_max * (1 - (u/u_max)**p)

# initialbetingelse u0(x) (fra oppgave a)
u0 = np.where(x < 0, u_max, 0.0)

# tegner grafen
fig, ax = plt.subplots(figsize=(10, 6))
lines = [ax.plot(x, u0, label=f'p={p}')[0] for p in p_values]
ax.set_ylim(-0.02, u_max + 0.05)
ax.set_title("Trafikkflyt etter grønt lys")
ax.set_xlabel("Posisjon x (meter)")
ax.set_ylabel("Tetthet u (biler/meter)")
ax.legend()

# lagring av data for animasjon
u_data = [u0.copy() for _ in p_values]

def update(frame):
    global u_data
    new_u_data = []
    
    for idx, p in enumerate(p_values):
        u = u_data[idx]
        u_next = np.zeros_like(u)
        
        # lax-Friedrichs skjema
        for j in range(1, len(x) - 1):
            # u_neste = 0.5*(u_høyre + u_venstre) - (dt/2dx)*(J_høyre - J_venstre)
            term1 = 0.5 * (u[j+1] + u[j-1])
            term2 = (dt / (2 * dx)) * (flux(u[j+1], p) - flux(u[j-1], p))
            u_next[j] = term1 - term2
            
        # randbetingelser
        u_next[0] = 0   # u(-1000, t) = 0 (veien tømmes bakfra)
        u_next[-1] = 0  # u(1000, t) = 0 (fri flyt foran)
        
        lines[idx].set_ydata(u_next)
        new_u_data.append(u_next)
    
    u_data = new_u_data
    return lines

ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()