import os
import time
from pathlib import Path

import geopandas as gpd
import numpy as np
import osmnx as ox
import pandas as pd
import params as par
import shapely as shp

from . import createLinksAndNodes as cln
from . import getPopulation as gp
from . import setActionsAndTransitions as actrans


def createBoundingBox(
    area={"north": 33.58, "south": 33.53, "east": 133.58, "west": 133.52}
):
    """
    Purpose:
        Creates a Bounding Box from a dictionary of NSEW geographical coordinates
    Returns:
        A shapely geometry"""
    bbox = shp.geometry.box(area["west"], area["south"], area["east"], area["north"])
    return bbox


def createGraph(
    area={"north": 33.58, "south": 33.53, "east": 133.58, "west": 133.52},
    crs="EPSG:6690",
    ntype="drive",
    plot=False,
):
    # Degree 1.0 = 111km. 2.22km x 4.44km square.
    # Obtain the roadmap data from OpenStreetMap by using OSMNX
    G = ox.graph_from_bbox(
        area["north"],
        area["south"],
        area["east"],
        area["west"],
        network_type=ntype,
        simplify=True,
    )
    G_projected = ox.project_graph(G, to_crs=crs)
    # Simplify topology
    G_simple = ox.simplification.consolidate_intersections(
        G_projected,
        tolerance=10,
        rebuild_graph=True,
        dead_ends=False,
        reconnect_edges=True,
    )
    # save the OSM data as Geopackage
    par.GRAPH_FILE = Path(par.CASE_FOLDER, "graph.gpkg")
    ox.io.save_graph_geopackage(G_simple, filepath=par.GRAPH_FILE)
    print(
        f"""The graph was saved as 'graph.gpkg' with projection {crs}.
This is a simplified {ntype} type OSM network."""
    )
    # Draw a map
    if plot:
        ox.plot_graph(G_simple, bgcolor="white", node_color="red", edge_color="black")

    # Create edges file
    edges = gpd.read_file(par.GRAPH_FILE, layer="edges")
    edges.to_file(Path(par.CASE_FOLDER, "edges.shp"))
    nedges = G.number_of_edges()
    print(f"{nedges} edges in graph. The edges file was saved as ESRI shapefile")
    return G_simple


def linksAndNodes(plot=False):
    # create database of links and edges
    cln.main()
    print("Database created!")
    if plot:
        cln.plotNetwork()


def getPrefShelters(pref_code=39, crs="EPSG:6690", filters=False):
    rootfolder = par.SHELTER_DATA_ROOT_FOLDER
    datafolder = par.SHELTER_DATA_FOLDER
    areafile = f"{pref_code:02d}/PHRP{pref_code:02d}18.shp"
    path = os.path.join(rootfolder, datafolder, areafile)
    shelters_gc = gpd.read_file(path, encoding="shift_jis")
    shelters = shelters_gc.to_crs(crs)
    if filters:
        shelters = shelters[shelters[par.FILTER_KEY] == 1]
    return shelters


def getAreaShelters(
    area={"north": 33.58, "south": 33.53, "east": 133.58, "west": 133.52},
    pref_code=39,
    crs="EPSG:6690",
    filter_bool=False,
):
    bbox = createBoundingBox(area)
    bbox_gdf = gpd.GeoSeries(bbox)
    bbox_gdf.set_crs(par.WK_CRS, inplace=True)
    bbox_gdf = bbox_gdf.to_crs(crs)
    poly = shp.geometry.shape(bbox_gdf[0])
    shelters = getPrefShelters(pref_code, crs, filters=filter_bool)
    gs = gpd.GeoSeries(shelters.geometry)
    sh_in_area = shelters[gs.within(poly)]
    return sh_in_area


def pointsWithinPolygon(poly):
    # Get the nodes within a polygon
    df = pd.read_csv(Path(par.CASE_FOLDER, "nodesdb.csv"))
    nodes = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.coord_x, df.coord_y), crs=par.PJ_CRS
    )
    gs = gpd.GeoSeries(nodes.geometry)
    ninarea = nodes[gs.within(poly)]
    return ninarea


def add_shelters(shelters_id=[337]):
    all_nodes = pd.read_csv(
        Path(par.CASE_FOLDER, "nodesdb0.csv"), names=["number", "coord_x", "coord_y"]
    )
    df_shelters = all_nodes[all_nodes["number"].isin(shelters_id)]
    shelters = gpd.GeoDataFrame(
        data=df_shelters,
        geometry=gpd.points_from_xy(x=df_shelters.coord_x, y=df_shelters.coord_y),
    )
    return shelters


def fixLinksDBAndNodesDB(shelters):
    # fixes the nodesdb to add shelters as nodes
    # requires 'shelters' geodataframe
    # the 'nodesdb.csv' was created with 'createLinksAndNodes.py'
    nodesnp = np.loadtxt(Path(par.CASE_FOLDER, "nodesdb0.csv"), delimiter=",")
    linksdb = np.loadtxt(Path(par.CASE_FOLDER, "linksdb0.csv"), delimiter=",")
    # create a numpy array for nodesdb
    nodesdb = np.zeros((nodesnp.shape[0], nodesnp.shape[1] + 2))
    nodesdb[:, :3] = nodesnp[:, :3]
    nodesdb[:, 4] += 1  # general reward
    # create a pandas then numpy for shelter coords
    sheltersdb = pd.DataFrame()
    for i, g in zip(shelters.index, shelters["geometry"]):
        x, y = g.coords.xy
        sheltersdb.loc[i, "x"], sheltersdb.loc[i, "y"] = x[0], y[0]
    sheltersdb = sheltersdb.to_numpy()
    for i in range(sheltersdb.shape[0]):
        x0, y0 = sheltersdb[i, :]
        dist = ((nodesnp[:, 1] - x0) ** 2 + (nodesnp[:, 2] - y0) ** 2) ** 0.5
        indx = np.argmin(dist)
        nodesdb[indx, 3] = 1
        nodesdb[indx, 4] = 1000  # shelter reward
    # correcting links length = 0 to = 2
    linksdb[:, 3][np.where(linksdb[:, 3] == 0)] = 2
    np.savetxt(
        Path(par.CASE_FOLDER, "nodesdb.csv"),
        nodesdb,
        delimiter=",",
        header="number,coord_x,coord_y,evacuation,reward",
        fmt="%d,%.6f,%.6f,%d,%d",
    )
    np.savetxt(
        Path(par.CASE_FOLDER, "linksdb.csv"),
        linksdb,
        delimiter=",",
        header="number,node1,node2,length,width",
        fmt="%d,%d,%d,%d,%d",
    )
    return


def appendAgents(agentsdb, pop, index, poly):
    # Get a polygon
    poly_pop = pop[par.POPULATION_FIELDNAME_IN_FILE].to_list()[index]
    ninarea = pointsWithinPolygon(poly)
    if ninarea.shape[0] == 0:
        return agentsdb
    pop_per_node = int(poly_pop / ninarea.shape[0])
    from_row = np.trim_zeros(agentsdb[:, 4], "b").shape[0]
    to_row = from_row + ninarea.shape[0] * pop_per_node  # +1?
    n = ninarea["# number"].to_list()
    nr = np.repeat(n, pop_per_node)
    agentsdb[from_row:to_row, 4] = nr
    return agentsdb


def cleanup():
    # Create folders
    par.DATA_FOLDER = Path(par.CASE_FOLDER, "data")
    par.REF_FOLDER = Path(par.CASE_FOLDER, "ref")
    par.WEIGHT_FOLDER = Path(par.CASE_FOLDER, "weights")
    Path(par.DATA_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(par.REF_FOLDER).mkdir(parents=True, exist_ok=True)
    Path(par.WEIGHT_FOLDER).mkdir(parents=True, exist_ok=True)
    # Move files
    currentdir = Path(par.CASE_FOLDER)
    for file in currentdir.glob("*.geojson"):
        file.rename(Path(par.REF_FOLDER, file.name))
    for file in currentdir.glob("*.csv"):
        file.rename(Path(par.DATA_FOLDER, file.name))
    for file in currentdir.glob("edges.*"):
        file.rename(Path(par.REF_FOLDER, file.name))
    for file in currentdir.glob("*.gpkg"):
        file.rename(Path(par.REF_FOLDER, file.name))


def run(aos_gdf):
    # AREA OF STUDY
    par.BBOX = {
        "north": aos_gdf.total_bounds[3],
        "south": aos_gdf.total_bounds[1],
        "east": aos_gdf.total_bounds[2],
        "west": aos_gdf.total_bounds[0],
    }

    # Get a Bounding Box of the area
    # bbox = createBoundingBox(area=area)
    # aos = gpd.GeoSeries([bbox]).to_json()

    # POPULATION
    # Get Population in the Area of Study (Census Data)
    if par.CENSUS_FROM_FILE_BOOL:
        pop = gpd.read_file(par.CENSUS_FILE)
    else:
        pop = gp.getPopulationArea(
            par.PREF_CODE, par.AOS_FILE, par.WK_CRS, par.BEFORE_2011_BOOL
        )
    pop_pj = pop.to_crs(par.PJ_CRS)

    # ROAD NETWORK
    if par.ROAD_NETWORK_FROM_FILE_BOOL:
        nodes = gpd.read_file(par.NODES_FILE)
        edges = gpd.read_file(par.EDGES_FILE)
        edges_pj = edges.to_crs(par.PJ_CRS)
        edges_pj.to_file(Path(par.CASE_FOLDER, "edges.shp"))
    else:
        # Create a Graph object
        G = createGraph(area=par.BBOX, crs=par.PJ_CRS, ntype=par.OSM_NTYPE, plot=False)
        nodes, edges = ox.graph_to_gdfs(G)

    # Create database of links and nodes
    linksAndNodes(plot=False)

    # SHELTERS
    if par.SHELTERS_FROM_FILE_BOOL:
        shelters = gpd.read_file(par.SHELTERS_FILE)
        shelters.to_crs(par.PJ_CRS, inplace=True)
    else:
        # Create a Shelter GeoDataframe
        shelters = getAreaShelters(
            area=par.BBOX,
            pref_code=par.PREF_CODE,
            crs=par.PJ_CRS,
            filter_bool=par.FILTER_SHELTER_BOOL,
        )
        if shelters.empty:
            print("There are no shelters in the area. Input a list of node ids")
            # try block to handle the exception
            if par.SHELTER_ID_BOOL:
                shelters_id = par.SHELTER_ID_LIST
            else:
                try:
                    shelters_id = []
                    while True:
                        shelters_id.append(
                            int(
                                input(
                                    "Enter a node number to become shelter or ENTER: "
                                )
                            )
                        )
                # if the input is not-integer, just print the list
                except:
                    print("Shelter nodes:", shelters_id)
                    shelters = add_shelters(shelters_id)

    # Fix the nodesdb to add shelters
    fixLinksDBAndNodesDB(shelters)

    # REINFORCEMENT LEARNING RELATED
    # Setup Actions and Transition Matrices
    actrans.setMatrices()

    # AGENTS
    if par.CENSUS_FROM_FILE_BOOL:
        pass
    else:
        par.POPULATION_FIELDNAME_IN_FILE = "TotalPop"
    print(
        f"There is a population of {int(pop[par.POPULATION_FIELDNAME_IN_FILE].sum())} people."
    )
    # Create the agentsdb
    agentsdb = np.zeros((int(pop[par.POPULATION_FIELDNAME_IN_FILE].sum()), 5))
    for i, g in enumerate(pop_pj.geometry.to_list()):
        agentsdb = appendAgents(agentsdb, pop=pop_pj, index=i, poly=g)
    last = np.trim_zeros(agentsdb[:, 4], "b").shape[0]
    agentsdb = agentsdb[:last, :]
    np.savetxt(
        Path(par.CASE_FOLDER, "agentsdb.csv"),
        agentsdb,
        delimiter=",",
        header="age,gender,hhType,hhId,Node",
        fmt="%d,%d,%d,%d,%d",
    )

    return pop, shelters, edges, nodes
