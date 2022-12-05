import os
import time
import warnings

import params as par
import source

warnings.simplefilter(action="ignore")  # , category=FutureWarning)

if __name__ == "__main__":
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

# Use this command to run in terminal
# python runner.py |& tee log.txt
