import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# parametere
v_max = 22.2  # m/s (80 km/t)
u_max = 0.2   # biler/meter (5m per bil)
L = 1000      # strekningen [-1000, 1000]
dx = 10       # vstand mellom punkter (h)
dt = 0.1      # tidssteg (k) - må overholde dt <= dx/v_max
t_slutt = 200  # økt tid for at bilen skal rekke å starte
x = np.arange(-L, L + dx, dx)
t_verdier = np.arange(0, t_slutt, dt)
p_values = [1, 2, 5]

# fluks funksjonen J
def flux(u, p):
    # J(u) = u * v(u)
    return u * v_max * (1 - (u/u_max)**p)

# initialtilstand
u0 = np.where(x < 0, u_max, 0.0)

# lagre data for hver p
results = {}

for p in p_values:
    u = u0.copy()
    p_bil = -980.0
    u_hist = []
    p_hist = []
    v_hist = []
    
    for t in t_verdier:
        # lagre nåværende tilstand for animasjon
        u_hist.append(u.copy())
        
        # finn fart og oppdater bilens posisjon
        u_lokal = np.interp(p_bil, x, u)
        v_bil = v_max * (1 - (u_lokal/u_max)**p)
        p_bil += dt * v_bil
        
        p_hist.append(p_bil)
        v_hist.append(v_bil)
        
        # oppdater trafikkfeltet (lax-friedrichs)
        u_neste = np.zeros_like(u)
        for j in range(1, len(x) - 1):
            u_neste[j] = 0.5*(u[j+1] + u[j-1]) - (dt/(2*dx))*(flux(u[j+1], p) - flux(u[j-1], p))
        
        # randbetingelser: veien tømmes i begge ender
        u_neste[0] = u_max
        u_neste[-1] = 0
        u = u_neste
        
    results[p] = {'u': u_hist, 'p': p_hist, 'v': v_hist}


# tegner grafer for d) 
fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
for p in p_values:
    ax1.plot(t_verdier, results[p]['p'], label=f'p={p}')
    ax2.plot(t_verdier, results[p]['v'], label=f'p={p}')

ax1.set_title("Posisjon P(t)")
ax1.legend()
ax2.set_title("Hastighet V(t)")
ax2.legend()
plt.tight_layout()
plt.show()