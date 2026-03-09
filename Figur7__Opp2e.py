import numpy as np
import matplotlib.pyplot as plt


v_max = 22.2  
u_max = 0.2   
L = 1000      
dx = 10       
dt = 0.1      
t_slutt = 250 # Vi simulerer lenge nok til at alle rekker å starte

x = np.arange(-L, L + dx, dx)
t_verdier = np.arange(0, t_slutt, dt)
p_values = [1, 2, 5]

# fluks funksjonen J
def flux(u, p): 
    return u * v_max * (1 - (u/u_max)**p)

# initialtilstand
u0 = np.where(x < 0, u_max, 0.0)

# resultatene
results = {p: {'K_t': []} for p in p_values}
t_stopp_liste = []


for p in p_values:
    u = u0.copy()
    bølge_nådd_slutt = False
    
    for i, t in enumerate(t_verdier):
        # finn bakerste punkt som har begynt å røre på seg
        moving_indices = np.where(u < 0.999 * u_max)[0]
        
        if len(moving_indices) > 0:
            K_t = x[moving_indices[0]]
        else:
            K_t = 0
            
        results[p]['K_t'].append(K_t)
        
        # sjekk om bølgen har nådd nesten helt til -1000
        if K_t <= -990 and not bølge_nådd_slutt:
            t_stopp_liste.append(t)
            bølge_nådd_slutt = True
        
        # lax-friedrichs 
        u_neste = np.zeros_like(u)
        for j in range(1, len(x) - 1):
            u_neste[j] = 0.5*(u[j+1] + u[j-1]) - (dt/(2*dx))*(flux(u[j+1], p) - flux(u[j-1], p))
        u_neste[0] = u_max 
        u_neste[-1] = 0
        u = u_neste

# finner ut når den tregeste bølgen (p=1) ble ferdig for å sette x-grensen
max_t_visning = max(t_stopp_liste) * 1.1 # legger på ca 10% margin

# tegner graf til e)
plt.figure(figsize=(10, 6))
for p in p_values:
    # plotter bare frem til bølgen nådde enden så den ikke blir for stor/lang
    plt.plot(t_verdier[:len(results[p]['K_t'])], results[p]['K_t'], label=f'Start-bølge K(t) for p={p}')

plt.axhline(-1000, color='r', linestyle='--', label='Kø-slutt (-1000m)')

# setter grensene slik at grafen slutter rett etter at alle er i gang
plt.xlim(0, max_t_visning)
plt.ylim(-1050, 50)

plt.title("Posisjonen til bilen som starter å bevege seg")
plt.xlabel("Tid (sekunder)")
plt.ylabel("Posisjon på veien (meter)")
plt.legend()
plt.grid(True)
plt.show()

# printer svar på spørsmålet i oppgaven
for i, p in enumerate(p_values):
    print(f"For p={p}, er alle biler i bevegelse etter ca. {t_stopp_liste[i]:.1f} sekunder.")