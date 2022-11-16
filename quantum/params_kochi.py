# Input parameters
CASE_NAME = "kochi"
PREF_CODE = 39  # Miyagi is 4, Kochi is 39

# Run conditions
MULTIPLE_RUNS_BOOL = True  # ! requires a list in NUM_SIM_PER_BLOCK
SETUP_BOOL = True
CLIP_TO_AOS_BOOL = True
EMAIL_BOOL = True
BEFORE_2011_BOOL = False  # in case population should be before 3.11
SHELTER_ID_BOOL = False  # if True read list of nodes id from SHELTER_ID_LIST variable
# if False prompots for id nodes
SHELTER_ID_LIST = []

# Run options
WK_CRS = 4326  # working CRS in GCS
PJ_CRS = 6690  # projected CRS in UTM
OSM_NTYPE = "drive"  # type of network for OSM

# File locations
AOS_FILE = "/Volumes/Pegasus32/kochi/polygon/aos_kochi_small_crs4326.geojson"
CENSUS_FILE = "/Volumes/Pegasus32/kochi/census/kochi-shi_census_crs4326.geojson"
SHELTERS_FILE = "/Volumes/Pegasus32/kochi/evacuation/Kochi_EvacBldg_CRS4326.geojson"
MESH_FILE = "/Volumes/Pegasus32/kochi/mesh/GEOJSON/kochi-shi-mesh.geojson"
TOWN_FILE = "/Volumes/Pegasus32/kochi/town/shi/kochi-shi_town_crs4326.geojson"
EDGES_FILE = "/Volumes/Pegasus32/kochi/road/pref/kochi_edges_crs6690.geojson"
NODES_FILE = "/Volumes/Pegasus32/kochi/road/pref/kochi_nodes_crs6690.geojson"

# Scenario parameters
SIM_TIME = 30  # in minutes
MEAN_DEPARTURE = 15  # in minutes
NUM_START = 0  # to start from interemediate point
NUM_BLOCKS = 1  # to act GLIE in various blocks
NUM_SIM_PER_BLOCK = [1000]  # 5hr, 2d 2h, 20d

# Reinforcement Learning parameters
GLIE_PERCENTAGE = 1.0  # it was on 0.8
DISCOUNT_RATE = 0.9  # original 0.9
FREQ_HISTOGRAM = 108000  # every 10 sec is default
SURVIVE_REWARD = 100000  # original 100_000
DEAD_REWARD = -1000  # original 1_000
STEP_REWARD = -1  # original -1

################################################################
###################  DO NOT MODIFY THIS PARAMETERS #############
################################################################

CASE_FOLDER = ""
DATA_FOLDER = ""
REF_FOLDER = ""
START_DATE = None
GRAPH_FILE = None
