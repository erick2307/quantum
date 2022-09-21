import time
from pathlib import Path

import numpy as np
import params as par

from .qlearn import QLearning


def run_ql_mod(simtime, meandeparture, numSim0, numBlocks, simPerBlock, name):
    t0 = time.time()
    agentsProfileName = Path(par.DATA_FOLDER, "agentsdb.csv")
    nodesdbFile = Path(par.DATA_FOLDER, "nodesdb.csv")
    linksdbFile = Path(par.DATA_FOLDER, "linksdb.csv")
    transLinkdbFile = Path(par.DATA_FOLDER, "actionsdb.csv")
    transNodedbFile = Path(par.DATA_FOLDER, "transitionsdb.csv")
    folderStateNames = Path(par.CASE_FOLDER, f"state_{name}")
    Path(folderStateNames).mkdir(parents=True, exist_ok=True)
    meanRayleighTest = meandeparture * 60
    simulTime = simtime * 60  # step is in seconds
    survivorsPerSim = []

    if numSim0 == 0:
        randomChoiceRate = 0.99
        optimalChoiceRate = 1.0 - randomChoiceRate
        case = QLearning(
            agentsProfileName=agentsProfileName,
            nodesdbFile=nodesdbFile,
            linksdbFile=linksdbFile,
            transLinkdbFile=transLinkdbFile,
            transNodedbFile=transNodedbFile,
            meanRayleigh=meanRayleighTest,
            discount=par.DISCOUNT_RATE,
        )

        totalagents = np.sum(case.pedDB.shape[0])

        for t in range(int(min(case.pedDB[:, 9])), simulTime):
            case.initEvacuationAtTime()
            case.stepForward()
            optimalChoice = bool(
                np.random.choice(2, 1, p=[randomChoiceRate, optimalChoiceRate])
            )
            case.checkTarget(ifOptChoice=optimalChoice)
            if not t % par.FREQ_HISTOGRAM:
                case.computePedHistDenVelAtLinks()
                case.updateVelocityAllPedestrians()

        outfile = Path(folderStateNames, "sim_%09d.csv" % numSim0)
        case.exportStateMatrix(outnamefile=outfile)
        print(
            f"""\n\n ***** Simu {numSim0:d}
              (t= {(time.time()-t0):.2f} sec.)*****"""
        )
        print("epsilon greedy - exploration: %f" % randomChoiceRate)
        print(
            f"""survived: {np.sum(case.pedDB[:,10] == 1)}
              / total: {totalagents}"""
        )

        survivorsPerSim.append([numSim0, np.sum(case.pedDB[:, 10] == 1)])
        fname = f"survivorsPerSim_{numBlocks}x{simPerBlock}.csv"
        outSurvivors = Path(folderStateNames, fname)
        np.savetxt(outSurvivors, np.array(survivorsPerSim), delimiter=",", fmt="%d")
        evacs_list = [evacs[1] for evacs in survivorsPerSim]
        print(
            f"""Max value:{max(evacs_list)},
              Index:{evacs_list.index(max(evacs_list))}"""
        )
        if survivorsPerSim[-1] == case.pedDB.shape[0]:
            return

        case = None

    numSim = numSim0 + 1
    for b in range(numBlocks):
        for s in range(simPerBlock):
            eoe = int(par.GLIE_PERCENTAGE * simPerBlock)  # end of exploration
            if s < eoe:
                randomChoiceRate = -1 / (eoe) ** 2 * s**2 + 1
            else:
                randomChoiceRate = 0.0
            optimalChoiceRate = 1.0 - randomChoiceRate
            case = QLearning(
                agentsProfileName=agentsProfileName,
                nodesdbFile=nodesdbFile,
                linksdbFile=linksdbFile,
                transLinkdbFile=transLinkdbFile,
                transNodedbFile=transNodedbFile,
                meanRayleigh=meanRayleighTest,
                discount=par.DISCOUNT_RATE,
            )
            index = evacs_list.index(max(evacs_list))
            namefile = Path(folderStateNames, "sim_%09d.csv" % index)
            case.loadStateMatrixFromFile(namefile=namefile)
            totalagents = np.sum(case.pedDB.shape[0])

            for t in range(int(min(case.pedDB[:, 9])), simulTime):
                case.initEvacuationAtTime()
                case.stepForward()
                optimalChoice = bool(
                    np.random.choice(2, 1, p=[randomChoiceRate, optimalChoiceRate])
                )
                case.checkTarget(ifOptChoice=optimalChoice)
                if not t % par.FREQ_HISTOGRAM:
                    case.computePedHistDenVelAtLinks()
                    case.updateVelocityAllPedestrians()

            outfile = Path(folderStateNames, "sim_%09d.csv" % numSim)
            case.exportStateMatrix(outnamefile=outfile)
            print(
                "\n\n ***** Simu %d (t= %.2f sec.)*****" % (numSim, (time.time() - t0))
            )
            print("epsilon greedy - exploration: %f" % randomChoiceRate)
            print(
                f"""survived: {np.sum(case.pedDB[:,10] == 1)}
                  / total: {totalagents}"""
            )

            # evaluate survivors in simulation
            survivorsPerSim.append([numSim, np.sum(case.pedDB[:, 10] == 1)])
            fname = f"survivorsPerSim_{numBlocks}x{simPerBlock}.csv"
            outSurvivors = Path(folderStateNames, fname)
            np.savetxt(outSurvivors, np.array(survivorsPerSim), delimiter=",", fmt="%d")
            evacs_list = [evacs[1] for evacs in survivorsPerSim]
            print(
                f"""Max value:{max(evacs_list)},
                   Index:{evacs_list.index(max(evacs_list))}"""
            )
            if survivorsPerSim[-1] == case.pedDB.shape[0]:
                return
            case = None
            numSim += 1
    return


def run():
    simtime = par.SIM_TIME
    meandeparture = par.MEAN_DEPARTURE

    numSim0 = par.NUM_START
    numBlocks = par.NUM_BLOCKS
    simPerBlock = par.NUM_SIM_PER_BLOCK

    name = f"{simtime}_{meandeparture}_{simPerBlock}"

    run_ql_mod(
        simtime=simtime,
        meandeparture=meandeparture,
        numSim0=numSim0,
        numBlocks=numBlocks,
        simPerBlock=simPerBlock,
        name=name,
    )
