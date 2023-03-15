import glob
import pandas as pd
import numpy as np
import params as par
import cmcrameri.cm as cmc
import matplotlib.pyplot as plt


def plot_weights(filename):
    accw = np.loadtxt(filename, skiprows=1, delimiter=",", usecols=1)
    N, bins, patches = plt.hist(accw, bins=[-1, 0, 1, 5, 10, 25, 50, 100], log=True)
    # Random facecolor for each bar
    color = cmc.bilbao(np.linspace(0, 1, len(N)))
    for i in range(len(N)):
        patches[i].set_facecolor(color[i])
    plt.title(
        f"Max evacuees at links during simulation {par.SIM_TIME}-{par.MEAN_DEPARTURE}"
    )
    plt.xlabel(f"Number of evacuees")
    plt.ylabel(f"Frequency")
    plt.xticks(ticks=bins[2:], labels=bins[2:], rotation=45)
    plt.savefig(f"{filename[:-4]}.png", dpi=300)
    return


def create_acc_weights():
    cases = sorted(glob.glob(f"./{par.CASE_FOLDER}/weights/*.csv"))
    df = pd.read_csv(cases[0], names=["link", "weight"])
    w = np.zeros((df.shape[0], 2), dtype=np.int16)
    w[:, 0] = df.link

    for case in cases[1:]:
        df = pd.read_csv(case, names=["link", "weight"])
        for i in range(df.shape[0]):
            if w[i, 1] < df["weight"].iloc[i]:
                w[i, 1] = df["weight"].iloc[i]

    wdf = pd.DataFrame(w, columns=["link", "weight"])
    bins = [-1, 0, 1, 5, 10, 25, 50, 100]
    s = wdf.groupby(pd.cut(wdf["weight"], bins=bins)).size()

    filename = f"./{par.CASE_FOLDER}/{par.CASE_FOLDER}_accw.csv"
    wdf.to_csv(filename, index=False)
    plot_weights(filename)
    return
