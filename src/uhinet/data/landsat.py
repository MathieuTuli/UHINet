from argparse import ArgumentParser

import logging

import ee.mapclient
import ee

parser = ArgumentParser(description=__doc__)
parser.add_argument('--log-level', default='INFO',
                    type=str)

args = parser.parse_args()
if args.log_level == 'INFO':
    logging.root.setLevel(logging.INFO)
elif args.log_level == 'DEBUG':
    logging.root.setLevel(logging.DEBUG)

if __name__ == "__main__":
    ee.Initialize()

    # item = ee.ImageCollection('LANDSAT/LC08/C01/T1') \
    #          .filterDate('2017-01-01', '2017-12-31') \
    #          .select(['B10', 'B11'])
    # print(item)

    landsat = ee.Image('LANDSAT/LE07/C01/T1_SR/LE07_044034_19990707')
    # .select(['B10'])
    # .filterDate('2017-01-01', '2017-12-31') \
    geometry = ee.Geometry.Rectangle([43.945970, -79.477810,
                                      43.654350, -79.407530])

    task = ee.batch.Export.image.toDrive(
            image=landsat,
            region=geometry.getInfo()['coordinates'],
            description='Download Lansdat from GEE',
            folder='landsat-data',
            fileNamePrefix='landsat_test',
            scale=30)
    # crs=myCRS)
    task.start()
    print(task.status())
