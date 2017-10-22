import json
import os
import sys
import argparse
from geopy.distance import great_circle


def load_data(input_file):
    with open(input_file, 'r', encoding='utf-8') as bars_json_file:
        try:
            return json.load(bars_json_file)
        except ValueError:
            return None


def get_biggest_bar(bars_list):
    return max(bars_list,
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_smallest_bar(bars_list):
    bars_list_with_seats = filter(
        lambda x: x['properties']['Attributes']['SeatsCount'] != 0,
        bars_list)
    return min(bars_list_with_seats,
               key=lambda x: x['properties']['Attributes']['SeatsCount'])


def get_closest_bar(bars_list, longitude, latitude):
    return min(bars_list,
               key=lambda bar: great_circle(
                   (longitude, latitude),
                   (bar['geometry']['coordinates'])).meters)


def get_formatted_bar_info(bar):
    bar_name = bar['properties']['Attributes']['Name']
    bar_address = bar['properties']['Attributes']['Address']
    return 'это {}, расположенный по адресу: {}'.format(bar_name,
                                                        bar_address)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath',
                        help="Input file for bars json data (Full path)",
                        required=True)
    parser.add_argument('--longtitude', help="Longtitude coordinate",
                        type=float, required=True)
    parser.add_argument('--latitude', help="latitude coordinate",
                        type=float, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    bars_json_data = None
    if os.path.isfile(args.filepath):
        bars_json_data = load_data(args.filepath)
    if bars_json_data:
        list_of_bars = bars_json_data.get('features')
        biggest_bar = get_biggest_bar(list_of_bars)
        print('Самый большой бар {}'.format(
            get_formatted_bar_info(biggest_bar)))
        smallest_bar = get_smallest_bar(list_of_bars)
        print('Самый маленький бар {}'.format(
            get_formatted_bar_info(smallest_bar)))
        jps_coordinates = (args.longtitude, args.latitude)
        closest_bar = get_closest_bar(list_of_bars, *jps_coordinates)
        print('Ближайший бар {}'.format(
            get_formatted_bar_info(closest_bar)))
    else:
        print("Ничего не найдено, проверьте файл")
