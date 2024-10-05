import dataExperiment as experiment
from matplotlib import pyplot as plt
import os

# experiment dataset
pathDataset = "./30_08_2024__11_29_47__Тест_ВАХ_2.txt"
dataset = experiment.readDataset(pathDataset)

# plot experiment graphs
all_IV_plot = 1
all_IV_with_mean_plot = 1
all_IV_with_mean_set_reset_plot = 1
grad_plot_plot = 1

nameFolderOutput = "30_08_2024__11_29_47__Тест_ВАХ_2.txt"
savePlots = 1
savePath = f"./experimentPlots/{nameFolderOutput}"

showPlots = 1

if savePlots:
    if not os.path.exists(savePath):
        os.makedirs(savePath)    

# plot graphs

if all_IV_plot:
    plt.figure(figsize=(13,7))
    plt.plot(dataset.U_allSignal, dataset.I_allSignal, label="experiment")
    plt.xlabel("U", fontsize=16)
    plt.ylabel("I", fontsize=16)
    plt.legend(fontsize=16)
    plt.grid()

    if savePlots:
        plt.savefig(f"{savePath}/all_IV.png")
    if showPlots:
        plt.show()

if all_IV_with_mean_plot:
    plt.figure(figsize=(13,7))
    plt.plot(dataset.U_allSignal, dataset.I_allSignal, label="experiment")
    plt.plot(dataset.U, dataset.I_mean, "-o", color="black", label="mean")
    plt.xlabel("U", fontsize=16)
    plt.ylabel("I", fontsize=16)
    plt.legend(fontsize=16)
    plt.grid()

    if savePlots:
        plt.savefig(f"{savePath}/all_IV_with_mean_plot.png")
    if showPlots:
        plt.show()

if grad_plot_plot:

    grad = dataset.getGradMean()

    plt.figure(figsize=(13,7))
    plt.plot(grad)
    plt.xlabel("number tap signal", fontsize=16)
    plt.ylabel("gradient", fontsize=16)
    plt.grid()

    if savePlots:
        plt.savefig(f"{savePath}/gradient.png")
    if showPlots:
        plt.show()

if all_IV_with_mean_set_reset_plot:
    plt.figure(figsize=(13,7))
    plt.plot(dataset.U_allSignal, dataset.I_allSignal, label="experiment")
    plt.plot(dataset.U, dataset.I_mean, "-o", color="black", label="mean")

    plt.axvline(dataset.u_set, ls="--", color="red", label="set voltage")
    plt.axvline(dataset.u_reset, ls="--", color="brown", label="reset voltage")

    plt.xlabel("U", fontsize=16)
    plt.ylabel("I", fontsize=16)
    plt.legend(fontsize=16, loc="upper left")
    plt.grid()

    if savePlots:
        plt.savefig(f"{savePath}/all_IV_with_mean_set_reset_plot.png")
    if showPlots:
        plt.show()        

