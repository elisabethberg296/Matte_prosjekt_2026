import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parametre
alpha = 1.37e-7     # termisk diffusitet for potet
lengde_x= 0.08
lengde_y = 0.04

#Antall punkter i x og y retning
Nx = 50
Ny = 25

#Avstand mellom punkter
dx = lengde_x/(Nx-1)
dy = lengde_y/(Ny-1)

dt = 0.1
steps = 10000
#plot_tidspkt = [600,3000,4500,6000]

# Initialbetingelse
u = np.ones((Ny, Nx)) * 15

# Lister for animasjon
frames = []
times = []

# Tidsiterasjon
for n in range(steps):
    # Randbetingelser
    u[:, 0] = 200
    u[:, -1] = 200
    u[0, :] = 200
    u[-1, :] = 200

    un = u.copy()

    u[1:-1,1:-1] = un[1:-1,1:-1] + alpha*dt*(
        (un[1:-1,2:] - 2*un[1:-1,1:-1] + un[1:-1,:-2])/dx**2 +
        (un[2:,1:-1] - 2*un[1:-1,1:-1] + un[:-2,1:-1])/dy**2
    )

    # lagrer noen frames til animasjon
    if n % 20 == 0:
        frames.append(u.copy())
        times.append(n * dt)


# Animasjon
fig, ax = plt.subplots()

im = ax.imshow(frames[0],
               origin="lower",
               cmap="coolwarm",
               extent=[0, lengde_x, 0, lengde_y],
               vmin=15, vmax=200)

plt.colorbar(im, ax=ax, label="Temperatur (°C)")
title = ax.set_title(f"Tid = {times[0]:.1f} s")

ax.set_xlabel("x")
ax.set_ylabel("y")

# Funksjon som oppdaterer bildet for hver frame
def update(i):
    im.set_array(frames[i])
    ax.set_title(f"Tid = {times[i]:.1f} s")
    return im,

# Lag animasjonen
ani = FuncAnimation(fig, update, frames=len(frames), interval=50, blit=False)

plt.show()