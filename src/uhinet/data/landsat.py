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
    ee.Initialize()
    img = ee.Image('LANDSAT/LT05/C01/T1_SR/LT05_034033_20000913')
    print(img)
    print(img.getInfo())
