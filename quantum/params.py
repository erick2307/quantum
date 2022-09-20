# Input parameters
CASE_NAME = "arahama"
PREF_CODE = 4  # Miyagi is 4, Kochi is 39

# Run conditions
SETUP_BOOL = True
CLIP_TO_AOS_BOOL = True
EMAIL_BOOL = True
BEFORE_2011_BOOL = True  # in case population should be before 3.11

# Run options
WK_CRS = 4326  # working CRS in GCS
PJ_CRS = 6691  # projected CRS in UTM
OSM_NTYPE = "drive"  # type of network for OSM

# File locations
AOS_FILE = "/Volumes/Pegasus32/arahama/polygon/arahama_aos.geojson"
CENSUS_FILE = "/Volumes/Pegasus32/arahama/census/arahama_census.geojson"
SHELTERS_FILE = "/Volumes/Pegasus32/arahama/buildings/arahama_bldgs_before2011.geojson"
MESH_FILE = "/Volumes/Pegasus32/arahama/mesh/arahama_mesh4.geojson"
TOWN_FILE = False  #'/Volumes/Pegasus32/kochi/town/shi/kochi-shi_town.shp'
EDGES_FILE = "/Volumes/Pegasus32/arahama/road/arahama_network.gpkg"
NODES_FILE = "/Volumes/Pegasus32/arahama/road/arahama_network.gpkg"

# Scenario parameters
SIM_TIME = 30  # in minutes
MEAN_DEPARTURE = 7  # in minutes
NUM_START = 0  # to start from interemediate point
NUM_BLOCKS = 1  # to act GLIE in various blocks
NUM_SIM_PER_BLOCK = 1000

# Reinforcement Leanring parameters
DISCOUNT_RATE = 0.9
FREQ_HISTOGRAM = 10  # every 10 sec is default
SURVIVE_REWARD = 100000
DEAD_REWARD = -1000
STEP_REWARD = -1

################################################################
###################  DO NOT MODIFY THIS PARAMETERS #############
################################################################

CASE_FOLDER = ""
DATA_FOLDER = ""
REF_FOLDER = ""
START_DATE = None
GRAPH_FILE = None
