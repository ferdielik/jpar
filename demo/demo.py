import json
import os

from src.pretty_parser import parse

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_data_from_file(path):
    data = open(os.path.join(__location__, path)).read()
    return json.dumps(json.loads(data), indent=2, sort_keys=True)


def parse_user(data_path, format_path):
    data = get_data_from_file(data_path)
    format = open(os.path.join(__location__, format_path)).read()
    return parse(format, data)


def main():
    results = []
    results.extend(parse_user('data/source1.json', 'format/source1_format.json'))
    results.extend(parse_user('data/source2.json', 'format/source2_format.json'))
    results.extend(parse_user('data/source3.json', 'format/source3_format.json'))
    print(results)


if __name__ == "__main__":
    # execute only if run as a script
    main()
