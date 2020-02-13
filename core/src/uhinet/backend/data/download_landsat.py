from calendar import monthrange
from pathlib import Path
import logging
import json
import cv2

from ..file_manager import save_pyplot_image, init_dirs, check_suffix, \
    file_exists
from .sentinel_hub import SentinelHubAccessor
from .components import ImageSize, LatLon
from .image_formatting import square_resize
from .helpers import conform_coordinates_to_spatial_resolution, get_seasons


def download_landsat_from_file(
        sentinelhub_accessor: SentinelHubAccessor,
        file_name: Path,
        save_to: Path) -> bool:
    '''
    file_name: Pathlib Path to .csv file
    '''

    if not file_exists(file_name) or not check_suffix(file_name, '.json'):
        return False
    with file_name.open() as f:
        content = json.load(f)

    valid_keys = ['centers', 'year_from', 'year_to',
                  'image_size', 'layers', 'cloud_coverage_percentage',
                  'spatial_resolution']
    for key in content.keys():
        if key not in valid_keys:
            logging.error(
                f"download_landsat: Invalid key \"{key}\". Must be one" +
                f" of {valid_keys}")
            return False
    centers = content['centers']

    # year_from, month_from, day_from = content['date_from'].split('-')
    # year_to, month_to, day_to = content['date_to'].split('-')
    # year_from = int(year_from)
    # month_from = int(month_from)
    # day_from = int(day_from)
    # year_to = int(year_to)
    # month_to = int(month_to)
    # day_to = int(day_to)
    year_from = int(content['year_from'])
    year_to = int(content['year_to'])

    image_height, image_width = content['image_size']
    layers = content['layers']
    image_size = ImageSize(height=image_height, width=image_width)
    cloud_cov_perc = float(content['cloud_coverage_percentage'])
    spatial_resolution = int(content['spatial_resolution'])

    seasons = get_seasons(year_from=year_from, year_to=year_to)
    for center in centers:
        location = LatLon(lat=center['lat'],
                          lon=center['lon'])
        # year = year_from
        # next_center = False
        for season in seasons:
            for layer in layers:
                imgs = sentinelhub_accessor.get_landsat_image(
                    layer=layer,
                    date=[season.date_from, season.date_to],
                    image_size=image_size,
                    cloud_cov_perc=cloud_cov_perc,
                    bbox=conform_coordinates_to_spatial_resolution(
                        spatial_resolution=spatial_resolution,
                        image_size=image_size,
                        center=location))
                if imgs is None:
                    logging.info(
                        "SentinelHubAccessor: No URL retrieved " +
                        f"for {center['name']} for {season.season}: " +
                        f"{season.date_from} to {season.date_to} and " +
                        f" {layer}.")
                else:
                    save_dir = save_to / \
                        f"{center['name']}/{season.year}/{str(season.season).lower()}"
                    init_dirs(save_dir)
                    logging.info(
                        "SentinelHubAccessor: URL retrieved " +
                        f"for {center['name']} for {season.season}: " +
                        f"{season.date_from} to {season.date_to} and " +
                        f" {layer}. Got {len(imgs)} images")
                    count = 0
                    for img in imgs:
                        img = square_resize(img, image_size[0], cv2.INTER_AREA)
                        save_pyplot_image(
                            save_dir /
                            f"{count}_{layer}.png",
                            img, cmap='Greys')
                        count += 1
    return True


if __name__ == "__main__":
    download_lansat_from_file(
        Path("landsat_all.json"))
