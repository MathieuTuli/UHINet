from pathlib import Path
from calendar import monthrange

import logging
import json
import cv2

from .file_manager import save_pyplot_image, init_dirs, check_suffix, \
    file_exists
from .SentinelHubAccessor import SentinelHubAccessor
from ..components import ImageSize, BBox, LatLon
from .image_formatting import square_resize

logging.root.setLevel(logging.INFO)
instance_id_path = Path("instance_id.txt")
if not instance_id_path.exists():
    logging.error(
        "download_landsat: Error: Instance id file not found. Please " +
        "create an \"instance_id.txt\" file.")


with instance_id_path.open() as f:
    instance_id = f.read().strip()

sentinelhub_accessor = SentinelHubAccessor(instance_id)


# TODO figure out optimal zoom
def download_lansat_from_file(file_name: Path) -> bool:
    '''
    file_name: Pathlib Path to .csv file
    '''

    if not file_exists(file_name) or check_suffix(file_name, '.json'):
        return False
    with file_name.open() as f:
        content = json.load(f)

    valid_keys = ['geometries', 'date_from', 'date_to',
                  'image_size', 'layers', 'cloud_coverage_percentage']
    for key in content.keys():
        if key not in valid_keys:
            logging.Error(
                f"download_landsat: Error: Invalid key \"{key}\". Must be one" +
                f" of {valid_keys}")
            return False
    geometries = content['geometries']

    year_from, month_from, day_from = content['date_from'].split('-')
    year_to, month_to, day_to = content['date_to'].split('-')
    year_from = int(year_from)
    month_from = int(month_from)
    day_from = int(day_from)
    year_to = int(year_to)
    month_to = int(month_to)
    day_to = int(day_to)

    image_height, image_width = content['image_size']
    layers = content['layers']
    image_size = ImageSize(height=image_height, width=image_width)
    cloud_cov_perc = float(content['cloud_coverage_percentage'])

    for geometry in geometries:
        bbox = BBox(top_left=LatLon(lat=geometry['tl_lat'],
                                    lon=geometry['tl_lon']),
                    bottom_right=LatLon(lat=geometry['br_lat'],
                                        lon=geometry['br_lon']))
        year = year_from
        next_geometry = False
        while year <= year_to:
            save_dir = Path(f"data/images/{geometry['name']}/{year}")
            init_dirs(save_dir)
            if next_geometry:
                break
            for month in range(1, 13):  # Month is always 1..12
                if next_geometry:
                    break
                for day in range(1, monthrange(year, month)[1] + 1):
                    if year == year_from and month < month_from \
                            and day < day_from:
                        continue
                    if year == year_to and month == month_to and day > day_to:
                        next_geometry = True
                        break
                    for layer in layers:
                        logging.info(
                            "download_landsat: Message: Getting for " +
                            f"{geometry['name']} at " +
                            f"{year}-{str(month).zfill(2)}-" +
                            "{str(day).zfill(2)} and {layer}")
                        imgs = sentinelhub_accessor.get_landsat_image(
                            layer=layer,
                            date=f"{year}-{str(month).zfill(2)}-" +
                                 f"{str(day).zfill(2)}",
                            image_size=image_size,
                            cloud_cov_perc=cloud_cov_perc,
                            bbox=bbox)
                        if imgs is not None:
                            count = 0
                            for img in imgs:
                                img = square_resize(img, 512, cv2.INTER_AREA)
                                save_pyplot_image(
                                    save_dir /
                                    f"{month}_{day}_{layer}_img_{count}.png",
                                    img)
                                count += 1
            year += 1
    return True


if __name__ == "__main__":
    download_lansat_from_file(
        Path("landsat_all.json"))
