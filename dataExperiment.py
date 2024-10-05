import numpy as np
from matplotlib import pyplot as plt

class DataExperimentIV():

    def __init__(self, U, I, settings):
        self.U = U[0:settings["numberPointInIV"]]
        self.U_allSignal = U
        self.I_allSignal = I
        self.settings = settings

        I_array = []
        for i in range(len(self.U_allSignal)):
            if i % settings["numberPointInIV"] == 0 and i != 0:
                I_array.append(np.array(I))
                I = []
            elif i == 0:
                I = []

            I.append(self.I_allSignal[i])

        # add last I
        I_array.append(np.array(I))
        self.I_matrix = np.array(I_array)

        self.I_mean = np.mean(self.I_matrix, axis=0)

        grad = self.getGradMean()

        idxSwitch1 = np.argmax(grad[0:len(grad)//2])
        idxSwitch2 = len(grad)//2+1 + np.argmax(grad[len(grad)//2+1:])

        if self.U[idxSwitch1] > self.U[idxSwitch2]:
            self.u_set = self.U[idxSwitch1]
            self.u_reset = self.U[idxSwitch2]
        else:
            self.u_set = self.U[idxSwitch2]
            self.u_reset = self.U[idxSwitch1]

        print(f"u_set = {self.u_set} \nu_reset = {self.u_reset}")


        grad_voltage = []
        for i in range(1, settings["numberPointInIV"]):
            grad_voltage.append(self.U[i] - self.U[i - 1])

        if settings["ampl_first"] > 0:
            idxsSetStart = 0
            idxSetEnd = int(settings["number_points_first"]) - 1

            idxResetStart = int(settings["number_points_first"])
            idxResetEnd = int(settings["number_points_first"]) + int(settings["number_points_second"]) - 1
            
            self.u_set_impulse = self.U[idxsSetStart:idxSetEnd+1]
            self.i_set_mean = self.I_mean[idxsSetStart:idxSetEnd+1]
            self.u_reset_impulse = self.U [idxResetStart:idxResetEnd+1]
            self.i_reset_mean = self.I_mean[idxResetStart:idxResetEnd+1]
        elif settings["ampl_second"] > 0:
            idxResetStart = 0
            idxResetEnd = int(settings["number_points_first"]) - 1

            idxsSetStart = int(settings["number_points_first"])
            idxSetEnd = int(settings["number_points_first"]) + int(settings["number_points_second"]) - 1
            
            self.u_set_impulse = self.U[idxsSetStart:idxSetEnd+1]
            self.i_set_mean = self.I_mean[idxsSetStart:idxSetEnd+1]
            self.u_reset_impulse = self.U [idxResetStart:idxResetEnd+1]
            self.i_reset_mean = self.I_mean[idxResetStart:idxResetEnd+1]

    def plotMeanIV(self):
        
        plt.figure(figsize=(13,7))
        plt.plot(self.U, self.I_mean, "-o")
        plt.grid()
        plt.show()

    def plotAllIV(self):

        plt.figure(figsize=(13,7))
        plt.plot(self.U_allSignal, self.I_allSignal)
        plt.grid()
        plt.show()

    def plotIVWithMean(self):
        
        plt.figure(figsize=(13,7))
        plt.plot(self.U_allSignal, self.I_allSignal, label="experiment")
        plt.plot(self.U, self.I_mean, "-o", color="black", label="mean")
        plt.legend(fontsize=16)
        plt.grid()
        plt.show()

    def getGradMean(self):
        grad = []
        for i in range(len(self.U)-1):
            grad_curr = (self.I_mean[i+1] - self.I_mean[i]) / np.abs(self.U[i+1] - self.U[i])
            grad.append(grad_curr)

        return grad

def readDataset(pathFile):

    settings = dict()
    data = dict()

    with open(pathFile) as f:
        lines = f.readlines()

    readData = 0
    for line in lines:
        if not readData:
            if "напляжение фаза 1" in line:
                settings["ampl_first"] = float(line.split()[4])
            if "напляжение фаза 2" in line:
                settings["ampl_second"] = float(line.split()[4])
            if "количество точек фаза 1" in line:
                settings["number_points_first"] = float(line.split()[4])
            if "количество точек фаза 2" in line:
                settings["number_points_second"] = float(line.split()[4])
            if "длительность импульсов" in line:
                settings["pulse_duration"] = float(line.split()[3])
            if "задержка между импульсами" in line:
                settings["impulse_delay"] = float(line.split()[4])
            if "количество ВАХ в файле" in line:
                settings["number_IV"] = int(line.split()[4])
            if "номер точки" in line:
                readData = 1

                data["num"] = []
                data["U"] = []
                data["I"] = []
        else:
            dataList = list(map(float, line.split()))
            data["num"].append(float(dataList[0]))
            data["U"].append(float(dataList[1]))
            data["I"].append(float(dataList[2]))


    numberPointInIV = int(len(data["U"]) / (settings["number_IV"]))
    settings["numberPointInIV"] = numberPointInIV
    dataset = DataExperimentIV(np.array(data["U"]), np.array(data["I"]), settings)

    return dataset