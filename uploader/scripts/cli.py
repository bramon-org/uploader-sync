import click
import glob
import requests
import json
import re
from uploader import data


def get_matching_captures(captures_dir: list):
    return glob.glob("{}/**/*".format(captures_dir), recursive=True)


def get_station_id(station_name: str):
    from uploader import data

    with open(data.STATIONS_MAP) as data_file:
        data = json.load(data_file)

    return list(filter(lambda x: x["name"] == station_name, data))


def get_station_name(capture):
    base = re.findall('(\w{3,5})_(\d{1,})(.+)?\.(\w{3})$', capture)

    if len(base) == 0:
        return False

    station = base[0][2].replace('_', '')

    # some files finish with A,M,P,T after station ID, remove it.
    fix = re.findall('(A|M|P|T)$', station)

    if len(fix) != 0:
        station = station[:-1]

    return station


def upload_captures(captures: list):
    for capture in captures:
        station_name = get_station_name(capture)

        if not station_name:
            continue

        station = get_station_id(station_name).pop()
        station_id = station['id']
        user_id = station['user_id']
        files = {'files[]': open(capture, 'rb')}
        values = {'station_id': station_id, 'user_id': user_id}
        headers = {'Authorization': "Bearer {}".format(data.API_TOKEN)}

        r = requests.post(data.API_URL, files=files, data=values, headers=headers)
        click.echo(r.text)


@click.command('uploader')
@click.argument('input_dir', type=click.Path(exists=True))
def cli(input_dir):
    click.echo('- Reading captures')
    captures = get_matching_captures(input_dir)

    if len(captures) == 0:
        click.echo("- Nothing to do")
        exit(0)

    click.echo("- Uploading captures")
    upload_captures(captures)

    click.echo("- Done :)")
