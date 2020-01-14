# MMCanada-Capstone

## A tool for predicting Urban Heat Island Effect, with a focus on the Greater Toronto Area

### Backend
Author: [Mathieu Tuli](https://github.com/MathieuTuli)

The backend follows a combination of a data and object oriented programming and provides the following features:
- data downloader for Landsat images. See the data section for how to use this functionality
- interface into the prediction model (training and testing interface)
- general file and data manipulators (converting metres into latitude/longitude coordinates, image concatenation, image resizing, etc.)


### Frontend
Authors: [Mathieu Tuli](https://github.com/MathieuTuli) & [Joe Sismondo](https://github.com/joesismondo) & [Quanzhou Li](https://github.com/licandow) & [Trevor Zhuang](https://github.com/zianaiz)

### Directory Structure
```
├── core                                          | Top entrypoint into the code.
│   ├── src                                       | Top directory for the UHINet package
│   │   ├── uhinet                                | UHINet module
│   │   │   ├── backend                           | UHINet backend module
│   │   │   │   ├── data                          | UHINet backend data module (landsat download, helpers for data manipulation)
│   │   │   │   │   └─── sentinel-hub-layers      | Javascript files for use in the SentinelHUB API for data downloading
│   │   │   │   ├── network                       | UHINet backend prediction module (training and testing)
│   │   │   ├── frontend                          | UHINet frontend module
│   │   │   │   ├── build                         | -
│   │   │   │   │   ├── static                    | Flask static: This directory contains the public CSS, JavaScript, images and other
│   │   │   │   │   └── templates                 | Flask templates: Jinja2 templates for our app
│   │   │   │   └── instance                      | Flask instance files live here (api keys, etc)
│   └── tests                                     | All test cases for pytest
```

### Installation

For mac-users, note that you will not be able to install the python `sentinelhub` package unless you have `geos` installed.
  To install `geos`, use brew... `brew install geos`

To use SentinelHub, perform the following
  1. Sign into the dashboard
  2. On the left-hand-side sidebar, access the `configuration utility` tab
  3. Add two new layers...
    - First layer is named `LST`, and all that needs to be done is to select `Landsat 8-L1C` as the source and copy-and-paste the `core/src/uhinet/backend/data/sentinel-hub-layers/lst.js` code into the code-editor.
    - Second layer is named `RGB`, and all that needs to be done is to select `Landsat 8-L1C` as the source and copy-and-paste the `core/src/uhinet/backend/data/sentinel-hub-layers/rgb.js` code into the code-editor or select, from the left-hand-side menu in the editor, `Base Product` then `TRUE_COLOR` and then the first `RGB visualization` option.
