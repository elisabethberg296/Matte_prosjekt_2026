import numpy as np
import matplotlib.pyplot as plt


# Parametre
h = 1e-6        # Presisjonskrav
xMin, xMax = -5, 5
yMin, yMax = 0, 2

# Antall punkter i rutenettet
Px = int((xMax-xMin)*15)
Py = int((yMax-yMin)*15)

x = np.linspace(xMin,xMax,Px)
y = np.linspace(yMin,yMax,Py)

u = np.zeros((Py,Px)) # Initialisering av løsningsmatrisen u (fylt med 0)

# Setter verdiene langs alle fire kanter
u[:,0] = np.sin(2*np.pi*y)
u[:,-1] = np.sin(2*np.pi*y)
u[0,:] = 0
u[-1,:] = np.sin(np.pi*x)

# Numerisk løsning (Iterativt)
for k in range(10000):      # Maks 10000 iterasjoner
    w = u.copy()            # Lagrer forrige steg for å sjekke endring

    # Går gjennom alle indre punkter
    for j  in range(1, Py-1):
        for i in range(1, Px-1):
            # Oppdaterer punktet som gjennsomsnittet av naboene
            u[j,i] = 0.25*(u[j,i+1] + u[j,i-1] + u[j+1,i] + u[j-1,i])
    error = np.max(abs(u-w)) # Sjekker om løsningen har stabilisert 
    if error < h:
        break

# Lager meshgrid
xx,yy = np.meshgrid(x,y)

# Bruker meshgrid til å lage 3D flate
ax =  plt.figure().add_subplot(projection='3d')
ax.plot_surface(xx,yy,u)
plt.show()

