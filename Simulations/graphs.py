import matplotlib.pyplot as plt
import statistics
import numpy as np
import math

ABRUNTIME = open("abruntime.txt")
ABSCORE = open("abgames.txt")

MMRUNTIME = open("mmruntime.txt")
MMSCORE = open("mmgames.txt")

WMRUNTIME = open("ogruntime.txt") 
WMSCORE = open("oggames.txt")


def score(file):
    scores = [0,0]
    for line in file:
        line.split()
        if line[0] > line[1]:
            scores[0] += 1

        if line[0] < line[1]:
            scores[1] += 1
    
    return scores

def score_bar_graph():
    barWidth = .25
    tickWidth = .125

    MM = score(MMSCORE)
    AB = score(ABSCORE)
    WM = score(WMSCORE)

    h = [MM[0], AB[0], WM[0]]
    c = [MM[1], AB[1], WM[1]]

    br1 = np.arange(len(h))
    br2 = [x + barWidth for x in br1]

    plt.bar(br1, h, color = 'r', width = barWidth, label = "Human")
    plt.bar(br2, c, color = 'b', width = barWidth, label = "Computer")

    plt.xlabel("Algorithm", fontsize = 14)
    plt.ylabel("Games Won", fontsize = 14)
    plt.xticks([r + tickWidth for r in range(len(h))], ["Minimax", "Alpha-Beta", "Weighted"])
    plt.title("Games Won out of 100 Game Simulation", fontsize = 18)
    plt.legend()
    plt.show()

score_bar_graph()

def runtime(file):
    file_data = []
    for line in file:
        line = float(line[:-2])
        if line == 0:
            pass
        else:
            line = line*1000
            file_data.append(line)

    return file_data

MMMEAN = statistics.mean(runtime(MMRUNTIME))
ABMEAN = statistics.mean(runtime(ABRUNTIME))
WMMEAN = statistics.mean(runtime(WMRUNTIME))

def runtimebargraph():
    data = []
    data.append(MMMEAN)
    data.append(ABMEAN)
    data.append(WMMEAN)

    labels = ["Minimax", "Alpha-Beta", "Weighted"]
    
    
    for i in range(len(labels)):
    
        label = "{:2.2f}".format(data[i])
        plt.annotate(label,(i, data[i]), xytext = (0,0), textcoords = "offset points", ha = "center")

    plt.bar(labels, data, color = 'r')
    plt.ylabel("ms", fontsize = 14)
    plt.xlabel("Algorithm", fontsize = 14)
    plt.title("Average Runtime Per Move", fontsize = 18)
    plt.show()
    
runtimebargraph()

def comp_graph():
    B = MMMEAN**(1/3) #branching factor
    DEPTH = np.linspace(0,3,100)

    abfactor = (math.log10(ABMEAN)/math.log10(B))/3
    
    ymm = B**DEPTH
    yab = B**(DEPTH/2)
    yabresult = B**(DEPTH*abfactor)
    yabavg = B**(DEPTH*.75)

    plt.plot(DEPTH,ymm, label = "Standard Minimax/AB")   #Minimax Standard

    plt.plot(DEPTH,yab, label = "Best Case AB")

    plt.plot(DEPTH,yabavg, label = "Average AB")
    
    plt.plot(DEPTH,yabresult, label = "Measured AB")

    plt.xlim(0,3)
    plt.ylabel("ms", fontsize = 14)
    plt.xlabel("Depth of Search", fontsize = 14)
    plt.title("Runtime as Function of Depth", fontsize = 18)
    plt.legend()
    plt.show()

comp_graph()