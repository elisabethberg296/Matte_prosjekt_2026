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

dt = 0.2
steps = 6001
plot_tidspkt = [600,3000,4500,6000]

# Initialbetingelse
u = np.ones((Ny, Nx)) * 15

mid_x = Nx//2
mid_y = Ny//2
funnet_60 = False

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

# Oppgave c - Sjekk når midten når 60°C
    if (not funnet_60) and u[mid_y, mid_x] >= 60:
        funnet_60 = True
        tid = n * dt
        print(f"Midten når 60°C ved t = {tid:.1f} s (n = {n})")

        # Varmeplot for dette tidpunktet
        plt.figure()
        plt.imshow(u, origin="lower", cmap="coolwarm",extent=[0, lengde_x, 0, lengde_y])
        plt.colorbar(label="Temperatur (°C)")
        plt.title(f"Midten når 60°C ved t = {tid:.1f} s")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
        break


        
