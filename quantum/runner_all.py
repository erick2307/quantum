import os
import time
import itertools
import warnings
import create_params as cp

warnings.simplefilter(action="ignore")  # , category=FutureWarning)


def define_cases(census=True):
    zones = [1]
    etas = [15, 30, 60]
    evacs = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    if not census:
        mss_days = [1]  # , 2, 3, 4, 5, 6, 7]  # mon, tue, wes, thu, fri, sat, sun
        mss_hours = [0, 6, 12, 18]
        all_lists = [zones, etas, evacs, mss_days, mss_hours]
    else:
        all_lists = [zones, etas, evacs]
    cases = list(itertools.product(*all_lists))
    return cases


def runner(current, total):
    import params as par
    import source

    if par.MULTIPLE_RUNS_BOOL:
        experiments = par.NUM_SIM_PER_BLOCK
        for i, exp in enumerate(experiments):
            start = time.time()
            source.dataset.run()
            print(f"Preprocess finished in {time.time() - start} sec.")
            source.process.run(simPerBlock=exp)
            filename = f"sim_{exp:09d}.csv"
            foldername = f"state_{par.SIM_TIME}_{par.MEAN_DEPARTURE}_{exp}"
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
                msg = f"Experiment {current}:{total} finished on {end:.2f} sec."
                source.send_email.SendMail(PASSWORD=pwd, MESSAGE=msg)


if __name__ == "__main__":
    cases = define_cases(census=False)
    print(f"There are {len(cases)} cases")
    for i, case in enumerate(cases):
        if (
            case == (1, 15, 1, 1, 0)
            or case == (1, 15, 1, 1, 6)
            or case == (1, 15, 1, 1, 12)
        ):
            continue
        if not case[1] <= case[2]:
            print(case)
            # CASE_NAME = f"Zone-{case[0]}-{case[1]}-{case[2]}",
            # AOS_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_mesh.geojson",
            # CENSUS_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_census.geojson",
            # SHELTERS_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_shelters.geojson",
            # EDGES_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_edges.geojson",
            # NODES_FILE = f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_nodes.geojson",
            # SIM_TIME=int(case[1]),  # in minutes
            # MEAN_DEPARTURE=int(case[2]),  # in minutes
            # NUM_SIM_PER_BLOCK=[100],
            # print(f"===============================================")
            # print(f"ZONE {case[0]} - ETA {case[1]} - EVAC {case[2]}")
            # print(f"===============================================")
            # ======================
            cp.create_params(
                CASE_NAME=f"Zone-{case[0]}-mssd-c{case[4]}-{case[1]}-{case[2]}",
                AOS_FILE=f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_mesh.geojson",
                CENSUS_FILE=f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_mssd_20220328{int(case[4]):02d}00.geojson",
                SHELTERS_FILE=f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_shelters.geojson",
                EDGES_FILE=f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_edges.geojson",
                NODES_FILE=f"/Volumes/Pegasus32/kochi/zones/zone0{case[0]}/z0{case[0]}_nodes.geojson",
                SIM_TIME=int(case[1]),  # in minutes
                MEAN_DEPARTURE=int(case[2]),  # in minutes
                NUM_SIM_PER_BLOCK=[100],
            )
            print(f"===============================================")
            print(f"ZONE {case[0]} - MSS {case[4]} - ETA {case[1]} - EVAC {case[2]}")
            print(f"===============================================")
            runner(i, len(cases))


# Use this command to run in terminal
# python runner.py |& tee log.txt
