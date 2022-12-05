# **Optimization of Tsunami Evacuation using Reinforcement Learning**

Last update: 2022.11.01

## **OBJECTIVE**

---

This repository prepares the data and runs a reinforcement learning-based tsunami evacuation optimization.

## **FOLDER STRUCTURE**

---
quantum  
 ┣ docs  
 ┃ ┣ `0_setup.ipynb`  
 ┃ ┣ `1_preprocess.ipynb`  
 ┃ ┗ `analysis.ipynb`  
 ┣ quantum  
 ┃ ┣ source  
 ┃ ┃ ┣ `__init__.py`  
 ┃ ┃ ┣ `createLinksAndNodes.py`  
 ┃ ┃ ┣ `dataset.py`  
 ┃ ┃ ┣ `getPopulation.py`  
 ┃ ┃ ┣ `preprocess.py`  
 ┃ ┃ ┣ `process.py`  
 ┃ ┃ ┣ `qlearn.py`  
 ┃ ┃ ┣ `send_email.py`  
 ┃ ┃ ┗ `setActionsAndTransitions.py`  
 ┃ ┣ `params.py`  
 ┃ ┗ `runner.py`  
 ┣ .gitattributes  
 ┣ .gitignore  
 ┣ LICENSE  
 ┣ README.md  
 ┣ quantum.txt  
 ┗ requirements.txt  

## **HOW TO USE IT**

---

1. Use `0_setup.ipynb` to [prepare your data](#prepare).
2. Modify the `params.py` file to model your case. See the [parameters description](#par_description) section.
3. Run `runner.py` file. Preferably in a *[tmux](https://github.com/tmux/tmux/wiki)* session.

<a id='prepare'></a>

### **1. Prepare your data**

:stop_sign: TODO

<a id='par_description'></a>

### **2. Parameters Description**

#### ***Input parameters***

`CASE_NAME` | `str` : The name of your case to run.  
`PREF_CODE` | `int` : The one or two digit code of Japan Prefecture. Used to get the population from Census Data.

### ***Run conditions***

`MULTIPLE_RUNS_BOOL` | `bool` : To run multiple scenarios of various epochs sequentially.  
~~`SETUP_BOOL` | `bool` : Not used?~~  
`CLIP_TO_AOS_BOOL` | `bool` :  Set `True` when the area of study (AOS) is smaller than the Prefecture size.  
`EMAIL_BOOL` | `bool` : Set `True` to receive email when simulation is done. The details of the email is in `send_email.py` file and the password should be in the environment variables.  
`BEFORE_2011_BOOL` | `bool` : If `True` extracts Census Data before the 2011 Great East Japan Earthquake and Tsunami.  
`SHELTER_ID_BOOL` | `bool` : If `True` reads list of nodes id for shelters from `SHELTER_ID_LIST`. If `False` prompts for id nodes.  i
`FILTER_SHELTER_BOOL` | `bool` : If `True` filters the kind of shelters to *TSUNAMI* shelters.  
`SHELTER_ID_LIST` | `list` of `int` : List of nodes id to consider as shelters.  

### ***Run options***

`WK_CRS` | `int` : A working CRS in GCS (e.g. 4326).  
`PJ_CRS` | `int` : A projected CRS in UTM (e.g. 6690).  
`OSM_NTYPE` | `str` : Network type from the OSM catalog (e.g. "drive").  

### ***File locations***

`AOS_FILE` | `geojson` : Polygon of the area of study. Used to get population and clip other data.  
`CENSUS_FILE` | `geojson` : A meshed file of population data.  
`SHELTERS_FILE` | `geojson` : A file with building data of shelters.  
`MESH_FILE` | `geojson` : Mesh4 file of the area of study.  
~~`TOWN_FILE` | `geojson` : Polygon file of administrative boudaries. Not used?~~  
~~`EDGES_FILE` | `geojson` : Network edges. Not used?~~  
~~`NODES_FILE` | `geojson` : Network nodes. Not used?~~  

### ***Scenario parameters***

`SIM_TIME` | `int` : Time in minutes for evacuation. Arrival time of tsunami may be used.  
`MEAN_DEPARTURE` | `int` : Mean of a Rayleigh distribution for the Departure Curve. A value in minutes).  
`NUM_START` | `int` : `0` when no previous output is used or a number of the state to the simulation.  
`NUM_BLOCKS` | `int` : Default to 1. These are blocks to apply GLIE.  
`NUM_SIM_PER_BLOCK` | `list` of `int` : Number of simulations at each block. Notice that the total number of episodes will be `NUM_BLOCKS` * `NUM_SIM_PER_BLOCK`.  

### ***Reinforcement Learning parameters***

`GLIE_PERCENTAGE` | `float` : Keep in 1.0.  
`DISCOUNT_RATE` | `float` : Default 0.9.  
`FREQ_HISTOGRAM` | `int` : Default 10. Frequency at which histograms of density are calculated in network edges to adjust evacuees' velocities. (in seconds).  
`SURVIVE_REWARD` | `int` : A reward value for actions at states in nodes that guided agents who reached shelters on time. Default 100_000 (Postitive).  
`DEAD_REWARD` | `int` : A penalty when the evacuation of an agent was not succesful. Default -1000 (Negative).  
`STEP_REWARD` | `int` : A penalty for time pressure in evacaution. Default -1 (Negative).  

## **TO DO**

:stop_sign: Add email and pwd as variables.  
