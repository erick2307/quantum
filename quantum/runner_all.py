import os
import time
import itertools
import warnings

import params as par
import source

warnings.simplefilter(action="ignore")  # , category=FutureWarning)


def define_cases(census=True):
    zones = [1, 2, 3, 4, 5]
    etas = [15, 30, 60]
    evacs = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    if not census:
        mss_days = [1, 2, 3, 4, 5, 6, 7]  # mon, tue, wes, thu, fri, sat, sun
        mss_hours = [0, 6, 12, 18]
        all_lists = [zones, etas, evacs, mss_days, mss_hours]
    else:
        all_lists = [zones, etas, evacs]
    cases = list(itertools.product(*all_lists))
    return cases


def runner():
    if par.MULTIPLE_RUNS_BOOL:
        experiments = par.NUM_SIM_PER_BLOCK
        for i, exp in enumerate(experiments):
            par.NUM_SIM_PER_BLOCK = exp
            start = time.time()
            source.dataset.run()
            print(f"Preprocess finished in {time.time() - start} sec.")
            source.process.run(simPerBlock=par.NUM_SIM_PER_BLOCK)
            filename = f"sim_{par.NUM_SIM_PER_BLOCK:09d}.csv"
            foldername = (
                f"state_{par.SIM_TIME}_{par.MEAN_DEPARTURE}_{par.NUM_SIM_PER_BLOCK}"
            )
            source.make_video.createVideo(
                filename=filename,
                foldername=foldername,
                area=par.CASE_FOLDER,
                simtime=par.SIM_TIME,
                meandeparture=par.MEAN_DEPARTURE,
            )
            if par.EMAIL_BOOL:
                pwd = os.environ.get(par.EMAIL_PWD)
                end = time.time() - start
                msg = f"Experiment {i}: {exp} runs finished on {end:.2f} sec."
                source.send_email.SendMail(PASSWORD=pwd, MESSAGE=msg)


if __name__ == "__main__":
    cases = define_cases(census=True)
    for case in cases:
        if not case[1] <= case[2]:
            par.CASE_NAME = f"Zone-{case[0]}-{case[1]}-{case[2]}"
            par.AOS_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_mesh.geojson"
            par.CENSUS_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_census.geojson"
            par.SHELTERS_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_shelters.geojson"
            par.EDGES_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_edges.geojson"
            par.NODES_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_nodes.geojson"
            print(f"===============================================")
            print(f"ZONE {case[0]} - ETA {case[1]} - EVAC {case[2]}")
            print(f"===============================================")
            runner()


# Use this command to run in terminal
# python runner.py |& tee log.txt
