import math as math
import matplotlib.pyplot as plt
import numpy as np

N_s = 4 #4 sensors
n = 2 #2 dimensions
#ref_s = 1 # number of reference sensor
sos = 346 #speed of sound

x_vals = [5, 8.5, 1.5, -4] # Spaltenvektoren sind Koordinaten
y_vals = [-3, 1.5, 1.5, 11]
z_vals = [0, 0, 0, 0]
t = [0.072485, 0.056672, 0.066191, 0.060762] #zeitstempel für jeden Sensor

def run_X_s():
    ref_s = 1
    #print(ref_s)

    R_iO = []
    for i in range(len(x_vals)):
        R_iO.append(math.sqrt(x_vals[i]**2+y_vals[i]**2+z_vals[i]**2))

    r_ij = np.array([((el*sos)-(t[ref_s-1]*sos)) for el in t])
    print(r_ij)


    if N_s == len(x_vals):
        print(True)
    else:
        print(False)

    S_j = np.matrix([[x_vals[el]-x_vals[ref_s-1] for el in range(len(x_vals)) if el != ref_s-1], [y_vals[el]-y_vals[ref_s-1] for el in range(len(y_vals)) if el != ref_s-1], [z_vals[el]-z_vals[ref_s-1] for el in range(len(z_vals)) if el != ref_s-1]])
    #print(S_j)
    #print(np.linalg.pinv(S_j)) #pseudoinverse der matrix, da S_j nicht invertierbar
    S_j = np.transpose(S_j)

    m_j = 0.5 * np.matrix([[(R_iO[el]**2) - (R_iO[ref_s-1]**2) - (r_ij[el]**2)] for el in range(N_s) if el != ref_s-1])
    print(m_j)
    print(m_j.shape)
    #print(np.transpose(m_j))

    rho_j = np.matrix([[r_ij[el] for el in range(N_s) if el != ref_s-1]])
    #print(rho_j)

    D_j = np.zeros((N_s - 1, N_s - 1), float)
    for el in range(N_s):
        # print(el)
        if el != ref_s - 1:
            D_j.flat[(el - 1) * N_s] = r_ij[el]
    # print(D_j)
    D_j = np.linalg.inv(D_j)

    I = np.identity(N_s-1)
    #print(I)

    Z = np.roll(I,1, axis=1)
    #print(Z)

    M_j = (I-Z)@D_j
    #print(M_j)

    X_s = np.linalg.pinv(np.transpose(S_j)@np.transpose(M_j)@M_j@S_j)@np.transpose(S_j)@np.transpose(M_j)@M_j@m_j
    #print(X_s)
    #print(X_s[0][0].item(),X_s[1][0].item())

    cols = ['red', 'green', 'blue', 'black']

    plt.figure(figsize=(10,10))
    plt.xlim(-20,20)
    plt.ylim(-20,20)

    for el in range(len(x_vals)):
        comp_x = [x_vals[el], X_s[0][0].item()]
        comp_y = [y_vals[el], X_s[1][0].item()]

        plt.plot(x_vals[el], y_vals[el], 'o', color=cols[el])
        plt.plot(comp_x, comp_y, ls=":", color=cols[el])

    plt.plot(X_s[0], X_s[1], 'o', color='cyan')

    plt.grid(True)
    plt.legend(["Sensor 1","1-Source","Sensor 2","2-Source", "Sensor 3","3-Source", "Sensor 4","4-Source", "Source"])
    plt.show()
    plt.close()

    return X_s[0][0].item(),X_s[1][0].item()

print("Coords:", run_X_s())

#Problem solved, program works