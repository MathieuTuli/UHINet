from pathlib import Path


if __name__ == "__main__":
    path = Path('/home/mat/work/U-of-T/capstone/uhinet/data/toronto-height/Boundaries/BuildingsBoundaries.csv')
    with path.open() as f:
        lines = f.readlines()
    print(lines[0])


