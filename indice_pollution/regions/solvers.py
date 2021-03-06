from importlib import import_module
from itertools import chain
import requests
import logging

regions = [
    'Auvergne-Rhône-Alpes',
    'Bretagne',
    'Corse',
    'Pays de la Loire',
    'Centre-Val de Loire',
    'Nouvelle-Aquitaine',
    'Hauts-de-France',
    'Grand Est',
    'Occitanie',
    'Île-de-France',
    'Sud',
    'Normandie'
]

def insee_list():
    return list(chain(*[
        import_module(f'.{region_name}', 'indice_pollution.regions').Forecast.insee_list()
        for region_name in regions
    ]))

def forecast(insee):
    r = requests.get(f'https://geo.api.gouv.fr/communes/{insee}', params={"fields": "region"})
    r.raise_for_status()
    region_name = r.json()['region']['nom']
    try:
        region = import_module(f'.{region_name}', 'indice_pollution.regions').Forecast()
    except ModuleNotFoundError:
        logging.error(f'Region {region_name} not found INSEE: {insee}')
        raise KeyError

    return region.get