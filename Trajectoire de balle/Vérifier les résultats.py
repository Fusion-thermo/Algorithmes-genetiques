from math import cos, sin, tan, pi
import numpy as np

V0=5 #arbitraire, peu importe cette valeur
g=9.81
max_haut=[0,0]
max_loin=[0,0]
max_rapport_vitesse=0
abscisses=np.linspace(0,100,5000)
for angle in range(90,-1,-1):
	i, y, alpha = 0, 0, angle*2*pi/360
	while y>=0:
		i+=1
		t=abscisses[i]
		x=V0*cos(alpha)*t
		y=V0*sin(alpha)*t-0.5*g*t**2
		if y>max_haut[1]:
			max_haut[0]=angle
			max_haut[1]=y
	if x>max_loin[1]:
		max_loin[0]=angle
		max_loin[1]=x
	print(angle,x/t)

print(max_haut,max_loin)