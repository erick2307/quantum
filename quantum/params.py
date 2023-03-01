# Input parameters
CASE_NAME = "Case"

# Set email for notifications
EMAIL_BOOL = True
SERVER_HOST = "server.jp"
PORT = 587
EMAIL = "name@email.jp"
EMAIL_PWD = "pwd"  # this is the name in the os environment variable

# Census data source
CENSUS_FROM_FILE_BOOL = True  # to use the file provided in CENSUS_FILE

POPULATION_FIELDNAME_IN_FILE = (
    "M_TOTPOP_H"  # for MSSD:"population"; for Census:"M_TOTPOP_H"
)
# If false needs to set below
BEFORE_2011_BOOL = False  # in case population should be before 3.11

# Shelter data source
SHELTERS_FROM_FILE_BOOL = True  # to use the file provided in SHELTERS_FILE
SHELTER_DATA_ROOT_FOLDER = "path/to/data/rootfolder" #PAREA HAZARD root folder
SHELTER_DATA_FOLDER = "path/to/datafolder" #PAREA HAZARD folder
# if false needs paramters below
SHELTER_ID_BOOL = False  # if True read list of nodes id from SHELTER_ID_LIST variable
# if False prompts for id nodes
FILTER_SHELTER_BOOL = True
FILTER_KEY = "str"
SHELTER_ID_LIST = []

# In case census or shelters are taken from database
PREF_CODE = 39  # Kochi is 39

# Run options
WK_CRS = 4326  # working CRS in GCS
PJ_CRS = 6690  # projected CRS in UTM

ROAD_NETWORK_FROM_FILE_BOOL = (
    True  # to use the file provided in EDGES_FILE and NODES_FILE
)
# if False needs parameter below
OSM_NTYPE = "drive"  # type of network for OSM

# File locations
AOS_FILE = "path/to/aos_file.geojson"
CENSUS_FILE = "path/to/census_file.geojson"
SHELTERS_FILE = "path/to/shelters_file.geojson"
EDGES_FILE = "path/to/edges_file.geojson"
NODES_FILE = "path/to/nodes_file.geojson"

# Scenario parameters
SIM_TIME = 20  # in minutes
MEAN_DEPARTURE = 5  # in minutes
NUM_START = 0  # to start from interemediate point
NUM_BLOCKS = 1  # to act GLIE in various blocks
MULTIPLE_RUNS_BOOL = True  # requires a list in NUM_SIM_PER_BLOCK
NUM_SIM_PER_BLOCK = [100, 1_000, 10_000]  # 5hr, 2d 2h, 20d

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
WEIGHT_FOLDER = ""
START_DATE = None
GRAPH_FILE = None
BBOX = None
