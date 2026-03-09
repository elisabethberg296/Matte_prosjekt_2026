import numpy as np
import matplotlib.pyplot as plt


v_max = 22.2  # m/s
u_max = 0.2   # biler/m (1bil/5meter)
u = np.linspace(0, u_max, 500)

# orginale funksjoner for hver verdi av p til sammenligning
v_orig1 = v_max * (1 - (u/u_max)**1)
v_orig2 = v_max * (1 - (u/u_max)**2)
v_orig5 = v_max * (1 - (u/u_max)**5)

def v1(u):
    return v_max*np.cos((np.pi*u)/(2*u_max)) # cosinus funksjonen 

print(v1(0)) 
print(v1(u_max)) 

def v2(u):
    return v_max * np.log(1+u_max-u)/np.log(1+u_max) # logaritme funksjonen 

print(v2(0))
print(v2(u_max)) 

# tegner grafen 
plt.figure(figsize=(10, 6))
plt.plot(u, v_orig1, label='Original (p=1)', color='pink', linestyle='--')
plt.plot(u, v_orig2, label='Original (p=2)', color='khaki', linestyle='--')
plt.plot(u, v_orig5, label='Original (p=5)', color='lightsalmon', linestyle='--')

plt.plot(u, v1(u), label='Cosinus-modell', color='teal', linewidth=2)
plt.plot(u, v2(u), label='Logaritme-modell', color='lime', linewidth=2)

plt.title("Alternative hastighetsfunksjoner v(u)")
plt.xlabel("Tetthet u (biler/m)")
plt.ylabel("Hastighet v (m/s)")
plt.legend()
plt.grid(True)
plt.show()