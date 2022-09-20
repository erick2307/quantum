import os
import time
import warnings

import params as par
import source

warnings.simplefilter(action="ignore")  # , category=FutureWarning)

if __name__ == "__main__":
    start = time.time()
    source.dataset.run()
    source.preprocess.run()
    source.process.run()
    if par.EMAIL_BOOL:
        pwd = os.environ.get("IRIDES_EMAIL_PWD")
        source.send_email.SendMail(PASSWORD=pwd)
