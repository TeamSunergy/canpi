import re
import polyline
import urllib
import simplejson
import pandas as pd
# from geopy.distance import vincenty
from urllib import request


ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json?locations=enc:'


def convert_path_to_polyline(path):
    polyline.encode(path, 5)


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_elevation_data(lat_lon_coords, **elvtn_args):
    key = 'AIzaSyCeoTnfT0MwM8M2sU9amxCZUBxr1Fn_RSQ'
    path_segments = []
    elevation_results = []
    df_route = pd.DataFrame(columns=['Lat', 'Lon', 'Elv'])
    for chunk in chunks(lat_lon_coords, 512):
        path_segments.append(chunk)
        path_string = ''
        for segments in path_segments:
            for lat, lon in segments:
                path_string = path_string + str(lat) + ',' + str(lon) + '|'
        path_string = path_string[0:-1]

        elvtn_args.update({
            'path': path_string,
            'samples': str(1),
        })
        """Change out all characters to be encoded with %s"""


        url = ELEVATION_BASE_URL + polyline.encode(chunk, 5) + '&key=' + key
        # print(url)
        response = simplejson.load(urllib.request.urlopen(url))

        # Create a dictionary for each results[] object
        elevation_result = []
        for resultset in response['results']:
            elevation_result.append(resultset['elevation'])
        elevation_results.append(elevation_result)

        # print(elevation_results)
    i = 0
    for segment_id, segments in enumerate(path_segments):
        j = 0
        for lat, lon in segments:
            df_route.loc[i] = pd.Series({'Lat': lat, 'Lon': lon, 'Elv': elevation_results[segment_id][j]})
            j += 1
            i += 1
    return df_route



def main(lat_lon_coords):
    df_route = get_elevation_data(lat_lon_coords)
    print(df_route)
    pass

if __name__ == '__main__':
    kml_file = "ASC 2016 (2).kml"
    with open(kml_file) as f:

        doc = f.read()

    split_doc = doc.split('\n')
    no_spaces = (i.replace(' ', '') for i in split_doc)
    regex = re.compile('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)', re.MULTILINE)
    lat_lon_coords = []
    for line in no_spaces:
        if regex.match(line):
            lon = line.split(',')[0]
            lat = line.split(',')[1]
            lat_lon_coords.append((float(lat), float(lon)))

    # print(doc)
    # print(lat_lon_coords)
    print(len(lat_lon_coords))
    main(lat_lon_coords)

    """
    
    Review the bottom of this page: https://developers.google.com/maps/documentation/elevation/intro
    and review this as well: https://github.com/googlemaps/js-v2-samples/blob/gh-pages/elevation/python/ElevationChartCreator.py
    
    """

