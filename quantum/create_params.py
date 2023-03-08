def create_params(
    CASE_NAME="Zone-1-30-15",
    MULTIPLE_RUNS_BOOL=True,
    SETUP_BOOL=None,
    CLIP_TO_AOS_BOOL=None,
    EMAIL_BOOL=True,
    SERVER_HOST="mail.irides.tohoku.ac.jp",
    PORT=587,
    EMAIL="mas@irides.tohoku.ac.jp",
    EMAIL_PWD="IRIDES_EMAIL_PWD",
    CENSUS_FROM_FILE_BOOL=True,
    POPULATION_FIELDNAME_IN_FILE="population",
    BEFORE_2011_BOOL=False,
    SHELTERS_FROM_FILE_BOOL=True,
    SHELTER_ID_BOOL=False,
    FILTER_SHELTER_BOOL=True,
    SHELTER_ID_LIST=[],
    PREF_CODE=39,
    WK_CRS=4326,
    PJ_CRS=6690,
    ROAD_NETWORK_FROM_FILE_BOOL=True,
    OSM_NTYPE="drive",
    AOS_FILE="/Volumes/Pegasus32/kochi/zones/zone01/z01_mesh.geojson",
    CENSUS_FILE="/Volumes/Pegasus32/kochi/zones/zone01/z01_census.geojson",
    SHELTERS_FILE="/Volumes/Pegasus32/kochi/zones/zone01/z01_shelters.geojson",
    MESH_FILE="/Volumes/Pegasus32/kochi/zones/zone01/z01_mesh.geojson",
    TOWN_FILE=None,
    EDGES_FILE="/Volumes/Pegasus32/kochi/zones/zone01/z01_edges.geojson",
    NODES_FILE="/Volumes/Pegasus32/kochi/zones/zone01/z01_nodes.geojson",
    SIM_TIME=30,
    MEAN_DEPARTURE=15,
    NUM_START=0,
    NUM_BLOCKS=1,
    NUM_SIM_PER_BLOCK=[100],
    GLIE_PERCENTAGE=1.0,
    DISCOUNT_RATE=0.9,
    FREQ_HISTOGRAM=10,
    SURVIVE_REWARD=100000,
    DEAD_REWARD=1000,
    STEP_REWARD=-1,
):
    text = f"""
# Input parameters
CASE_NAME = {repr(str(CASE_NAME))}

# Run conditions
MULTIPLE_RUNS_BOOL = {MULTIPLE_RUNS_BOOL}

# SETUP_BOOL = {SETUP_BOOL}
# CLIP_TO_AOS_BOOL = {CLIP_TO_AOS_BOOL}

# Set email for notifications
EMAIL_BOOL = {EMAIL_BOOL}
SERVER_HOST = {repr(str(SERVER_HOST))}
PORT = {PORT}
EMAIL = {repr(str(EMAIL))}
EMAIL_PWD = {repr(str(EMAIL_PWD))}  # this is the name in the os environment variable

# Census data source
CENSUS_FROM_FILE_BOOL = {CENSUS_FROM_FILE_BOOL}  # to use the file provided in CENSUS_FILE
POPULATION_FIELDNAME_IN_FILE = {repr(str(POPULATION_FIELDNAME_IN_FILE))}  # for MSSD:"population"; for Census:"M_TOTPOP_H"
# If false needs to set below
BEFORE_2011_BOOL = {BEFORE_2011_BOOL}  # in case population should be before 3.11

# Shelter data source
SHELTERS_FROM_FILE_BOOL = {SHELTERS_FROM_FILE_BOOL}  # to use the file provided in SHELTERS_FILE
# if false needs paramters below
SHELTER_ID_BOOL = {SHELTER_ID_BOOL}  # if True read list of nodes id from SHELTER_ID_LIST variable
# if False prompts for id nodes
FILTER_SHELTER_BOOL = {FILTER_SHELTER_BOOL}
SHELTER_ID_LIST = {SHELTER_ID_LIST}

# In case census or shelters are taken from database
PREF_CODE = {PREF_CODE}  # Miyagi is 4, Kochi is 39, Fukushima is 7

# Run options
WK_CRS = {WK_CRS}  # working CRS in GCS
PJ_CRS = {PJ_CRS}  # projected CRS in UTM

ROAD_NETWORK_FROM_FILE_BOOL = {ROAD_NETWORK_FROM_FILE_BOOL}  # to use the file provided in EDGES_FILE and NODES_FILE
# if False needs parameter below
OSM_NTYPE = {repr(str(OSM_NTYPE))}  # type of network for OSM

# File locations
AOS_FILE = {repr(str(AOS_FILE))}
CENSUS_FILE = {repr(str(CENSUS_FILE))}
SHELTERS_FILE = {repr(str(SHELTERS_FILE))}
# MESH_FILE = {repr(str(MESH_FILE))}
# TOWN_FILE = {repr(str(TOWN_FILE))}
EDGES_FILE = {repr(str(EDGES_FILE))}
NODES_FILE = {repr(str(NODES_FILE))}

# Scenario parameters
SIM_TIME = {int(SIM_TIME)}  # in minutes
MEAN_DEPARTURE = {int(MEAN_DEPARTURE)}  # in minutes
NUM_START = {int(NUM_START)}  # to start from interemediate point
NUM_BLOCKS = {int(NUM_BLOCKS)}  # to act GLIE in various blocks
NUM_SIM_PER_BLOCK = {NUM_SIM_PER_BLOCK}  # 5hr, 2d 2h, 20d

# Reinforcement Learning parameters
GLIE_PERCENTAGE = {float(GLIE_PERCENTAGE)}  # it was on 0.8
DISCOUNT_RATE = {float(DISCOUNT_RATE)}  # original 0.9
FREQ_HISTOGRAM = {int(FREQ_HISTOGRAM)}  # every 10 sec is default
SURVIVE_REWARD = {float(SURVIVE_REWARD)}  # original 100_000
DEAD_REWARD = {float(DEAD_REWARD)}  # original 1_000
STEP_REWARD = {float(STEP_REWARD)}  # original -1

################################################################
###################  DO NOT MODIFY THIS PARAMETERS #############
################################################################

CASE_FOLDER = ""
DATA_FOLDER = ""
REF_FOLDER = ""
WEIGHT_FOLDER = ""
START_DATE = None
GRAPH_FILE = None
BBOX = None
"""
    with open("params.py", "w") as params:
        params.write(text)
        params.close()

    print("Parameter file created")
    return


if __name__ == "__main__":
    pass
