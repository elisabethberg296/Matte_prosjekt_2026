import numpy as np
import matplotlib.pyplot as plt

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
steps = 6001
plot_tidspkt = [600,3000,4500,6000]

# Initialbetingelse
u = np.ones((Ny, Nx)) * 15

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

    if n in plot_tidspkt:
        plt.figure()
        plt.imshow(u, origin="lower", cmap="coolwarm",extent=[0, lengde_x, 0, lengde_y])
        plt.colorbar(label="Temperatur (°C)")
        plt.title(f"Tid = {n*dt:.0f} sekunder")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

