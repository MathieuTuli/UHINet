from pathlib import Path
from pyproj import Proj, transform

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
    path = Path(
        '/home/mat/Downloads/test/toronto_massing_wayback/3DMassing_2016_WGS84.shp')
    df = GeoDataFrame.from_file(str(path))
    print(df.keys())
    df.rename(
        columns={
            'MIN_HEIGHT': 'MIN_HEIGHT',
            'MAX_HEIGHT': 'MAX_HEIGHT',
            'AVG_HEIGHT': 'HEIGHT',
            'HEIGHT_MSL': 'HEIGHT_ELEV',
            'SURF_ELEV': 'ELEV',
            'HEIGHT_SRC': 'HEIGHT_SRC',
            'BLDG_SRC': 'BLDG_SRC',
            'LONGITUDE': 'LONGITUDE',
            'LATITUDE': 'LATITUDE',
            'POLY_AREA': 'POLY_AREA',
            'PERIMETER': 'PERIMETER',
            'geometry': 'geometry'},
        inplace=True)
    df.drop(['MIN_HEIGHT', 'MAX_HEIGHT', 'HEIGHT_SRC',
             'BLDG_SRC', 'LONGITUDE', 'LATITUDE', 'PERIMETER'], axis=1,
            inplace=True)
    print(df.head())
    df.to_crs({'init': 'epsg:4326'}, inplace=True)
    print(df.head())
    df.to_file(
        '/home/mat/work/U-of-T/capstone/uhinet/data/toronto-height/Boundaries/2019_formatted.shp', driver='ESRI Shapefile')

    path = Path(
        '/home/mat/Downloads/test/toronto_massing_wayback/3DMassing_2017_WGS84.shp')
    df = GeoDataFrame.from_file(str(path))
    print(df.keys())
    path = Path(
        '/home/mat/Downloads/test/toronto_massing_wayback/3DMassing_2018_WGS84.shp')
    df = GeoDataFrame.from_file(str(path))
    print(df.keys())
    path = Path(
        '/home/mat/Downloads/test/toronto_massing_wayback/SHAPEFILES/ContextMassing2013_mtm3degree_v2.shp')
    df = GeoDataFrame.from_file(str(path))
    print(df.keys())
    path = Path(
        '/home/mat/Downloads/test/toronto_massing_wayback/SHAPEFILES/ContextMassing2013_wgs84_v2.shp')
    df = GeoDataFrame.from_file(str(path))
    print(df.keys())
    path = Path(
        '/home/mat/Downloads/test/toronto_massing_wayback/ODMassing_2014_wgs.shp')
    df = GeoDataFrame.from_file(str(path))
    print(df.keys())
    #                     df_2019 = GeoDataFrame.from_file(str(path))
    #                     df_2019.rename(
    #                         columns={
    #                             'MIN_HEIGHT': 'MIN_HEIGHT',
    #                             'MAX_HEIGHT': 'MAX_HEIGHT',
    #                             'AVG_HEIGHT': 'HEIGHT',
    #                             'HEIGHT_MSL': 'HEIGHT_ELEV',
    #                             'SURF_ELEV': 'ELEV',
    #                             'HEIGHT_SRC': 'HEIGHT_SRC',
    #                             'BLDG_SRC': 'BLDG_SRC',
    #                             'LONGITUDE': 'LONGITUDE',
    #                             'LATITUDE': 'LATITUDE',
    #                             'POLY_AREA': 'POLY_AREA',
    #                             'PERIMETER': 'PERIMETER',
    #                             'geometry': 'geometry'},
    #                         inplace=True)
    #                     df_2019.drop(['MIN_HEIGHT', 'MAX_HEIGHT', 'HEIGHT_SRC',
    #                                   'BLDG_SRC', 'LONGITUDE', 'LATITUDE', 'PERIMETER'], axis=1,
    #                                  inplace=True)
    #                     print(df_2019.head())
    #                     df_2019.to_crs({'init': 'epsg:4326'}, inplace=True)
    #                     print(df_2019.head())
    #                     df_2019.to_file(
    #                         '/home/mat/work/U-of-T/capstone/uhinet/data/toronto-height/Boundaries/2019_formatted.shp', driver='ESRI Shapefile')
    #      df_2019 = GeoDataFrame.from_file('2019.shp')
    #      fig, ax = plt.subplots(1, 1)
    #      df_2019.plot(column='HEIGHT', ax=ax, legend=True, cmap='tab20')
    #      plt.show()
    # import fiona
    # print(fiona.supported_drivers)
    # df_2019.to_file("2019.shp")
    # df = GeoDataFrame.from_File("2019.shp", driver='ESRI Shapefile')

    # pat1 = Path('/home/mat/Downloads/test/toronto_massing_wayback/3DMassing_2016_WGS84.shp')

    # boros1 = GeoDataFrame.from_file(str(pat1))
    # boros = GeoDataFrame.from_file(str(path))
    # print(boros.keys())
    # boros = boros.sort_values(by='MAX_HEIGHT', ascending=True)
    # boros1 = boros.sort_values(by='Z', ascending=True)
    # boros = boros.set_index('MAX_HEIGHT')
    # boros = boros.sort_index()

    # Plot and color by borough
    # fig, ax = plt.subplots(1, 1)
    # # boros1.plot(column='EleZ', ax=ax, legend=True, cmap='tab20')
    # boros.plot(column='AVG_HEIGHT', ax=ax, legend=True, cmap='tab20')
    # plt.show()
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
