# Input parameters
CASE_NAME = "koriyama"
PREF_CODE = 7  # Miyagi is 4, Kochi is 39, Fukushima is 7

# Run conditions
MULTIPLE_RUNS_BOOL = True  # ! requires a list in NUM_SIM_PER_BLOCK
SETUP_BOOL = True
CLIP_TO_AOS_BOOL = False
EMAIL_BOOL = False
BEFORE_2011_BOOL = False  # in case population should be before 3.11
SHELTER_ID_BOOL = False  # if True read list of nodes id from SHELTER_ID_LIST variable
# if False prompots for id nodes
FILTER_SHELTER_BOOL = False
SHELTER_ID_LIST = []

# Run options
WK_CRS = 4326  # working CRS in GCS
PJ_CRS = 6691  # projected CRS in UTM
OSM_NTYPE = "walk"  # type of network for OSM

# File locations
AOS_FILE = (
    "/Volumes/Pegasus32/koriyama/small_area/polygon/koriyama_small_aos_crs4326.geojson"
)
CENSUS_FILE = None  # "/Volumes/Pegasus32/kochi/census/kochi-shi_census_crs4326.geojson"
SHELTERS_FILE = "/Volumes/Pegasus32/koriyama/small_area/evacuation/koriyama_small_shelters_crs4612.geojson"
MESH_FILE = "/Volumes/Pegasus32/koriyama/small/mesh/koriyama_small_mesh_crs4326.geojson"
TOWN_FILE = None  # "/Volumes/Pegasus32/kochi/town/shi/kochi-shi_town_crs4326.geojson"
EDGES_FILE = None  # "/Volumes/Pegasus32/kochi/road/pref/kochi_edges_crs6690.geojson"
NODES_FILE = None  # "/Volumes/Pegasus32/kochi/road/pref/kochi_nodes_crs6690.geojson"

# Scenario parameters
SIM_TIME = 20  # in minutes
MEAN_DEPARTURE = 5  # in minutes
NUM_START = 0  # to start from interemediate point
NUM_BLOCKS = 1  # to act GLIE in various blocks
NUM_SIM_PER_BLOCK = [10]  # 5hr, 2d 2h, 20d

# Reinforcement Learning parameters
GLIE_PERCENTAGE = 1.0  # it was on 0.8
DISCOUNT_RATE = 0.9  # original 0.9
FREQ_HISTOGRAM = 10  # every 10 sec is default
SURVIVE_REWARD = 100_000  # original 100_000
DEAD_REWARD = -1_000  # original 1_000
STEP_REWARD = -1  # original -1

################################################################
###################  DO NOT MODIFY THIS PARAMETERS #############
################################################################

CASE_FOLDER = ""
DATA_FOLDER = ""
REF_FOLDER = ""
START_DATE = None
GRAPH_FILE = None


def verify():
    from pathlib import Path

    try:
        Path(AOS_FILE).is_file()
    except:
        print(f"AOS_FILE = {AOS_FILE} does not exist")

    try:
        Path(CENSUS_FILE).is_file()
    except:
        print(f"CENSUS_FILE = {CENSUS_FILE} does not exist")

    try:
        Path(SHELTERS_FILE).is_file()
    except:
        print(f"SHELTER_FILE = {SHELTERS_FILE} does not exist")

    try:
        Path(MESH_FILE).is_file()
    except:
        print(f"MESH_FILE = {MESH_FILE} does not exist")

    try:
        Path(TOWN_FILE).is_file()
    except:
        print(f"TOWN_FILE = {TOWN_FILE} does not exist")

    try:
        Path(EDGES_FILE).is_file()
    except:
        print(f"EDGES_FILE = {EDGES_FILE} does not exist")

    try:
        Path(NODES_FILE).is_file()
    except:
        print(f"NODES_FILE = {NODES_FILE} does not exist")
    return


def show():
    print(
        f"""
CASE = {CASE_NAME}
PREF_CODE = {PREF_CODE}
MULTIPLE_RUNS_BOOL = {MULTIPLE_RUNS_BOOL}
SETUP_BOOL = {SETUP_BOOL}
CLIP_TO_AOS_BOOL = {CLIP_TO_AOS_BOOL}
EMAIL_BOOL = {EMAIL_BOOL}
BEFORE_2011_BOOL = {BEFORE_2011_BOOL}
SHELTER_ID_BOOL = {SHELTER_ID_BOOL}
SHELTER_ID_LIST = {SHELTER_ID_LIST}

WK_CRS = {WK_CRS}
PJ_CRS = {PJ_CRS}
OSM_NTYPE = {OSM_NTYPE}

*** FILE PATH ***
AOS_FILE = {AOS_FILE}
CENSUS_FILE = {CENSUS_FILE}
SHELTERS_FILE = {SHELTERS_FILE}
MESH_FILE = {MESH_FILE}
TOWN_FILE = {TOWN_FILE}
EDGES_FILE = {EDGES_FILE}
NODES_FILE = {NODES_FILE}

*** SCENARIO ***
SIM_TIME = {SIM_TIME}
MEAN_DEPARTURE = {MEAN_DEPARTURE}
NUM_START = {NUM_START}
NUM_BLOCKS = {NUM_BLOCKS}
NUM_SIM_PER_BLOCK = {NUM_SIM_PER_BLOCK}
      
** RL ***      
GLIE_PERCENTAGE = {GLIE_PERCENTAGE}
DISCOUNT_RATE = {DISCOUNT_RATE}
FREQ_HISTOGRAM = {FREQ_HISTOGRAM}
SURVIVE_REWARD = {SURVIVE_REWARD}
DEAD_REWARD = {DEAD_REWARD}
STEP_REWARD = {STEP_REWARD}"""
    )
    return
