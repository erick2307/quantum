from datetime import datetime
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import params as par
import source.preprocess as pre

plt.style.use("default")


def load_geojson(filename, crs):
    return gpd.read_file(filename, driver="GeoJSON").to_crs(crs)


def check_file(filename):
    if bool(filename):
        return True
    else:
        return False


def plot_census(data, ax=None, column="M_TOTPOP_H"):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    plt.tight_layout()
    data.plot(ax=ax, column=column, cmap="jet")
    return ax


def create_folder(dirname):
    Path(dirname).mkdir(parents=True, exist_ok=True)


def save_to_case_folder(data, filename, driver="GeoJSON"):
    if driver == "GeoJSON":
        data.to_file(Path(par.CASE_FOLDER, f"{filename}.geojson"), driver=driver)
    if driver == "SHP":
        data.to_file(Path(par.CASE_FOLDER, f"{filename}.shp"))


def get_case_date(timestamp):
    ms = timestamp / 1000.0
    return datetime.fromtimestamp(ms)


########################################################################
def run():
    # create a folder based on the date and case name
    par.START_DATE = datetime.now()
    par.CASE_FOLDER = f"{str(round(par.START_DATE.timestamp()*1000))}_{par.CASE_NAME}"
    create_folder(dirname=par.CASE_FOLDER)
    print(f"Case started on {par.START_DATE}")

    aos = gpd.read_file(par.AOS_FILE, driver="GeoJSON").to_crs(par.WK_CRS)
    census, shelters, edges, nodes = pre.run(aos)

    save_to_case_folder(aos, "aos")
    save_to_case_folder(census, "census")
    save_to_case_folder(shelters, "shelters")
    # save_to_case_folder(mesh, "mesh")
    # save_to_case_folder(edges, "edges", driver="SHP")
    # save_to_case_folder(nodes, "nodes", driver="SHP")
    # save_to_case_folder(town, "town")

    pre.cleanup()

    # if not check_file(par.CENSUS_FILE):
    #     # get census
    #     pass
    # census = gpd.read_file(par.CENSUS_FILE, driver="GeoJSON").to_crs(par.WK_CRS)
    # if not check_file(par.SHELTERS_FILE):
    #     # get shelters
    #     pass
    # shelters = gpd.read_file(par.SHELTERS_FILE, driver="GeoJSON").to_crs(par.WK_CRS)
    # if not check_file(par.MESH_FILE):
    #     # get mesh
    #     pass
    # mesh = gpd.read_file(par.MESH_FILE, driver="GeoJSON").to_crs(par.WK_CRS)
    # if not check_file(par.TOWN_FILE):
    #     # get town
    #     pass
    # town = gpd.read_file(par.TOWN_FILE, driver="GeoJSON").to_crs(par.WK_CRS)
    # if not check_file(par.EDGES_FILE):
    #     # get edges
    #     pass
    # edges = gpd.read_file(par.EDGES_FILE, driver="GeoJSON").to_crs(par.WK_CRS)
    # if not check_file(par.NODES_FILE):
    #     # get nodes
    #     pass
    # nodes = gpd.read_file(par.NODES_FILE, driver="GeoJSON").to_crs(par.WK_CRS)

    # if par.CLIP_TO_AOS_BOOL:
    #     census = census.clip(aos)
    #     shelters = shelters.clip(aos)
    #     mesh = mesh.clip(aos)
    #     town = town.clip(aos)
    #     edges = edges.clip(aos)
    #     nodes = nodes.clip(aos)
