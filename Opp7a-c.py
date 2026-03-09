import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

# Parametre og grid
t_max = 1700        # Antall tidssteg i simuleringsløkka

alfaLuft = 5e-5     # Termisk diffusivitet for luft
alfaKropp = 22e-5   # Termisk diffusivitet for legemet 

xyMin, xyMax = 0, 6     # Størrelse på simuleringsområdet (inkludert luftlag)
px, py = 100, 100       # Oppløsning (antall punkter i x og y)

x = np.linspace(xyMin, xyMax, px)
y = np.linspace(xyMin, xyMax, py)

h = (xyMax - xyMin) / (px - 1)      # Avstand mellom gridpunkter (dx og dy)

# Stabilitetskrav: k (dt) må være liten nok for at den numeriske metoden ikke skal divergere
k = 0.1 * h**2 / alfaKropp

# Initialbetingelser
oMin, oMax = 20, 80

u = np.ones((py, px, t_max)) * 200 # Starter på 200 grader
u[oMin:oMax, oMin:oMax, :] = 15 # Legemet settes inn med starttemp 15 grader

alfa = np.ones((py, px)) * alfaLuft
alfa[oMin:oMax, oMin:oMax] = alfaKropp

# Numerisk løsning (Varmeligningen)
for l in range(t_max - 1):
    # Regner ut neste tidssteg (u_t = alfa * nabla^2 u)
    u[1:-1, 1:-1, l+1] = (
        u[1:-1, 1:-1, l]
        + (alfa[1:-1,1:-1] * k / h**2) * (
            u[2:, 1:-1, l]
            + u[:-2, 1:-1, l]
            + u[1:-1, 2:, l]
            + u[1:-1, :-2, l]
            - 4 * u[1:-1, 1:-1, l]
        )
    )
    # Randbetingelser: holdes konstant på 200 grader
    u[0,:,l+1] = 200
    u[-1,:,l+1] = 200
    u[:,0,l+1] = 200
    u[:,-1,l+1] = 200
    

# Analyse av temperatur i midten
mid = px // 2
midT = u[mid, mid, :] # Temperaturen i midten

if np.any(midT >= 60):
    t60 = np.argmax(midT >= 60) # Finner første tidssteg der temp >= 60
    sekund60 = t60 * k
else:
    t60 = -1
    sekund60 = None
    print("60 grader ble aldri nådd")

if t60 >= 0:
    # Plotter situasjonen når kjernen når 60 grader
    fig1, ax1 = plt.subplots()

    im1 = ax1.imshow(
        u[:,:,t60],
        cmap="coolwarm",
        origin="lower",
        extent=[xyMin, xyMax, xyMin, xyMax],
        vmin=np.min(u),
        vmax=np.max(u)
    )

    plt.colorbar(im1)
    ax1.set_title(f"Midten når 60°C etter {sekund60:.3f} sekunder")
    plt.show()


# Animasjon
fig, ax = plt.subplots()

im = ax.imshow(
    u[:,:,0],
    cmap="coolwarm",
    origin="lower",
    extent=[xyMin, xyMax, xyMin, xyMax],
    vmin=np.min(u),
    vmax=np.max(u)
)

plt.colorbar(im)

def update(frame):

    im.set_array(u[:,:,frame])
    ax.set_title(f"Tid = {frame*k:.3f} s")

    return [im]

animation = ani.FuncAnimation(
    fig,
    update,
    frames=t_max,
    interval=20,
    blit=False
)

plt.show()
