from pathlib import Path

from geopandas import GeoDataFrame, GeoSeries
from shapely.geometry import Point, Polygon
from matplotlib.colors import Normalize
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import geopandas


if __name__ == "__main__":
    path = Path('/home/mat/work/U-of-T/capstone/uhinet/data/toronto-height/Boundaries/3DMassingShapefile_2019_WGS84/3DMassing_2019_WGS84.shp')
    # Get the shape-file for NYC
    boros = GeoDataFrame.from_file(str(path))
    # boros = boros.set_index('MAX_HEIGHT')
    # boros = boros.sort_index()

    # Plot and color by borough
    fig, ax = plt.subplots(1, 1)
    boros.plot(column='MAX_HEIGHT', ax=ax, legend=True, cmap='tab20c')
    plt.show()
    # Get rid of are that you aren't interested in (too far away)
    # plt.gca().set_xlim([-74.05, -73.85])
    # plt.gca().set_ylim([40.65, 40.9])
    # 
    # # make a grid of latitude-longitude values
    # xmin, xmax, ymin, ymax = -74.05, -73.85, 40.65, 40.9
    # xx, yy = np.meshgrid(np.linspace(xmin,xmax,100), np.linspace(ymin,ymax,100))
    # xc = xx.flatten()
    # yc = yy.flatten()
    # 
    # # Now convert these points to geo-data
    # pts = GeoSeries([Point(x, y) for x, y in zip(xc, yc)])
    # in_map =  np.array([pts.within(geom) for geom in boros.geometry]).sum(axis=0)
    # pts = GeoSeries([val for pos,val in enumerate(pts) if in_map[pos]])
    # 
    # # Plot to make sure it makes sense:
    # pts.plot(markersize=1)
    # 
    # # Now get the lat-long coordinates in a dataframe
    # coords = []
    # for n, point in enumerate(pts):
    #     coords += [','.join(__ for __ in _.strip().split(' ')[::-1]) for _ in str(point).split('(')[1].split(')')[0].split(',')]
