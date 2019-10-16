from argparse import ArgumentParser

import logging

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
    # task = ee.batch.Export.image.toDrive(
    #         image=myImg,
    #         region=myRegion.getInfo()['coordinates'],
    #         description='myDescription',
    #         folder='myGDriveFolder',
    #         fileNamePrefix='myFilePrefix',
    #         scale=myScale,
    #         crs=myCRS)
    # task.start()
    # task.status()
    ee.Initialize()
