import numpy as np
from matplotlib import pyplot as plt
import dataExperiment as experiment
import fittingAlgorithms as fitAlg

dataset = experiment.readDataset("./30_08_2024__11_29_47__Тест_ВАХ_2.txt")
dataset.plotIVWithMean()

# search idx in first half signal
idx_set_hrs = np.where(dataset.u_set_impulse <= dataset.u_set)[0]
idx_set_hrs = np.where(idx_set_hrs < dataset.u_set_impulse.shape[0] // 2)[0]
idx_set_hrs = np.where(dataset.i_set_mean[idx_set_hrs] > 0)[0]

idx_reset_hrs = np.where(dataset.u_reset_impulse >= dataset.u_reset)[0]
idx_reset_hrs = np.where(idx_reset_hrs > dataset.u_reset_impulse.shape[0] // 2 + 20)[0]

u_set_hrs = dataset.u_set_impulse[idx_set_hrs]
i_set_hrs = dataset.i_set_mean[idx_set_hrs]

u_set_hrs_reg = u_set_hrs[:, np.newaxis]
u_set_hrs_reg = np.concatenate((u_set_hrs_reg, np.ones_like(u_set_hrs_reg)), axis=1)
i_set_hrs_reg = np.log(i_set_hrs[:, np.newaxis])

coeff = fitAlg.LS(u_set_hrs_reg, i_set_hrs_reg)

c3 = np.exp(coeff[1])
c4 = coeff[0]

u_reset_hrs = dataset.u_reset_impulse[idx_reset_hrs]
i_reset_hrs = dataset.i_reset_mean[idx_reset_hrs]

u_reset_hrs_reg = u_reset_hrs[:, np.newaxis]
u_reset_hrs_reg = np.concatenate((u_reset_hrs_reg, np.ones_like(u_reset_hrs_reg)), axis=1)
i_reset_hrs_reg = np.log(np.abs(i_reset_hrs[:, np.newaxis]))
# plt.figure(figsize=(13,8))
# plt.plot(u_reset_hrs_reg, i_reset_hrs_reg)
# plt.show()
coeff2 = fitAlg.LS(u_reset_hrs_reg, i_reset_hrs_reg)

c3_2 = np.exp(coeff2[1])
c4_2 = coeff2[0]
print(c3_2, c4_2)
plt.figure(figsize=(13,7))
plt.plot(u_reset_hrs, i_reset_hrs)
plt.plot(u_reset_hrs, -7.5147451e-06*np.exp((-1.89400278*u_reset_hrs)))
plt.show()

# exit(0)

print(f"coeff from LS equation with log current {coeff}")
print(f"find coeff for HRS from LS equation c3 = {c3}, c4 = {c4}")

plt.figure(figsize=(13,7))
plt.plot(u_set_hrs, i_set_hrs_reg)
plt.plot(u_set_hrs, c4*u_set_hrs + np.log(c3))
plt.grid()
plt.show()

plt.figure(figsize=(13,7))
plt.plot(u_set_hrs, i_set_hrs)
plt.plot(u_set_hrs, c3 * (np.exp(c4*u_set_hrs) - 1), '-o')
plt.grid()
plt.show()

plt.figure(figsize=(13,7))
plt.plot(dataset.U, dataset.I_mean)
# plt.plot(dataset.U, c3 * (np.exp(c4*dataset.U) - 1, '-o'))
plt.plot(np.linspace(0,0.85,50), c3 * (np.exp(c4*np.linspace(0,0.85,50)) - 1), 'x')
# plt.plot(np.linspace(-1.12,0,50), -7.5147451e-06*np.exp((-1.89400278*np.linspace(-1.12,0,50))), 'x')
plt.plot(np.linspace(-1,0,50), 0.000047*np.linspace(-1,0,50) + c3*np.exp((c4*np.linspace(-1,0,50)) - 1), 'x')
plt.plot(np.linspace(-1.12,0.85,50), 0.00047*np.linspace(-1.12,0.85,50) + c3 * (np.exp(c4*np.linspace(0,0.85,50)) - 1), 'x')

# plt.plot(np.linspace(-0.8,0,50), c3*np.exp((c4*np.linspace(-0.8,0,50)) - 1), 'x')

plt.legend([
    "mean data from experiment",
    "forward current from pn junction: 4.9e-7 * (exp(5.96*V) - 1)",
    "backword current from pn junction: 0.000047*V + 4.9e-7 * (exp(5.96*V) - 1)",
    "ON current: 0.00047*V + pn forward junction"
], fontsize=14)

plt.grid()

# plt.plot(dataset.U, 0.0005*(0.9**20)*dataset.U, '-x')

plt.show()