from . import ForecastMixin
from dateutil.parser import parse
import requests as requests_
from requests import adapters
import ssl
from urllib3 import poolmanager

class TLSAdapter(adapters.HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)


class Forecast(ForecastMixin):
    url = 'https://data.airbreizh.asso.fr/geoserver/ind_bretagne_agglo/ows'

    epci_agglo = {
        '242900314': 'ind_bretagne_agglo_BREST',
        '200042174': 'ind_bretagne_agglo_LORIENT',
        '200068120': 'ind_bretagne_agglo_QUIMPER',
        '243500139': 'ind_bretagne_agglo_RENNES',
        '200069409': 'ind_bretagne_agglo_SAINT_BRIEUC',
        '243500782': 'ind_bretagne_agglo_SAINT_MALO',
        '200067932': 'ind_bretagne_agglo_VANNES',
    }

    HTTPAdapter = TLSAdapter

    @classmethod
    def params(cls, date, insee):
        epci = cls.insee_epci[insee]
        agglo = cls.epci_agglo[epci]

        return {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typeName': f'ind_bretagne_agglo:{agglo}',
            'outputFormat': 'application/json',
            'CQL_FILTER': f"date_ech>'{date}'"
        }

    @classmethod
    def getter(cls, feature):
        return { 
            **{
                'indice': feature['properties']['valeur'],
                'date':str(parse(feature['properties']['date_ech']).date())
            },
            **{k: feature['properties'][k] for k in cls.outfields if k in feature['properties']}
        }

    @classmethod
    def insee_list(cls):
        return cls.insee_epci.keys()

    insee_epci = {
        "29019": "242900314",
        "29075": "242900314",
        "29189": "242900314",
        "29212": "242900314",
        "29235": "242900314",
        "29069": "242900314",
        "29061": "242900314",
        "29011": "242900314",
        "56121": "200042174",
        "56098": "200042174",
        "56162": "200042174",
        "56083": "200042174",
        "56078": "200042174",
        "56185": "200042174",
        "56107": "200042174",
        "56101": "200042174",
        "56036": "200042174",
        "56090": "200042174",
        "56166": "200042174",
        "56193": "200042174",
        "56118": "200042174",
        "56179": "200042174",
        "56040": "200042174",
        "56063": "200042174",
        "56181": "200042174",
        "56026": "200042174",
        "56069": "200042174",
        "56089": "200042174",
        "56188": "200042174",
        "56021": "200042174",
        "56029": "200042174",
        "56104": "200042174",
        "56062": "200042174",
        "29232": "200068120",
        "29051": "200068120",
        "29020": "200068120",
        "29170": "200068120",
        "29216": "200068120",
        "29169": "200068120",
        "29173": "200068120",
        "29048": "200068120",
        "29106": "200068120",
        "29066": "200068120",
        "29229": "200068120",
        "29107": "200068120",
        "29110": "200068120",
        "29134": "200068120",
        "35238": "243500139",
        "35047": "243500139",
        "35051": "243500139",
        "35281": "243500139",
        "35210": "243500139",
        "35024": "243500139",
        "35055": "243500139",
        "35278": "243500139",
        "35240": "243500139",
        "35334": "243500139",
        "35352": "243500139",
        "35066": "243500139",
        "35196": "243500139",
        "35206": "243500139",
        "35001": "243500139",
        "35353": "243500139",
        "35120": "243500139",
        "35139": "243500139",
        "35059": "243500139",
        "35275": "243500139",
        "35208": "243500139",
        "35131": "243500139",
        "35363": "243500139",
        "35032": "243500139",
        "35076": "243500139",
        "35245": "243500139",
        "35189": "243500139",
        "35088": "243500139",
        "35204": "243500139",
        "35266": "243500139",
        "35080": "243500139",
        "35079": "243500139",
        "35065": "243500139",
        "35039": "243500139",
        "35250": "243500139",
        "35216": "243500139",
        "35351": "243500139",
        "35315": "243500139",
        "35058": "243500139",
        "35144": "243500139",
        "35081": "243500139",
        "35180": "243500139",
        "35022": "243500139",
        "22278": "200069409",
        "22187": "200069409",
        "22215": "200069409",
        "22360": "200069409",
        "22106": "200069409",
        "22251": "200069409",
        "22055": "200069409",
        "22176": "200069409",
        "22389": "200069409",
        "22171": "200069409",
        "22081": "200069409",
        "22203": "200069409",
        "22325": "200069409",
        "22262": "200069409",
        "22277": "200069409",
        "22307": "200069409",
        "22372": "200069409",
        "22232": "200069409",
        "22117": "200069409",
        "22170": "200069409",
        "22281": "200069409",
        "22287": "200069409",
        "22059": "200069409",
        "22144": "200069409",
        "22099": "200069409",
        "22377": "200069409",
        "22386": "200069409",
        "22073": "200069409",
        "22291": "200069409",
        "22276": "200069409",
        "22009": "200069409",
        "22126": "200069409",
        "35288": "243500782",
        "35049": "243500782",
        "35299": "243500782",
        "35179": "243500782",
        "35263": "243500782",
        "35224": "243500782",
        "35284": "243500782",
        "35116": "243500782",
        "35306": "243500782",
        "35122": "243500782",
        "35070": "243500782",
        "35132": "243500782",
        "35279": "243500782",
        "35358": "243500782",
        "35362": "243500782",
        "35255": "243500782",
        "35314": "243500782",
        "35153": "243500782",
        "56260": "200067932",
        "56206": "200067932",
        "56243": "200067932",
        "56240": "200067932",
        "56251": "200067932",
        "56164": "200067932",
        "56053": "200067932",
        "56158": "200067932",
        "56003": "200067932",
        "56067": "200067932",
        "56008": "200067932",
        "56248": "200067932",
        "56231": "200067932",
        "56247": "200067932",
        "56137": "200067932",
        "56167": "200067932",
        "56262": "200067932",
        "56255": "200067932",
        "56132": "200067932",
        "56042": "200067932",
        "56005": "200067932",
        "56157": "200067932",
        "56115": "200067932",
        "56120": "200067932",
        "56214": "200067932",
        "56259": "200067932",
        "56022": "200067932",
        "56254": "200067932",
        "56252": "200067932",
        "56205": "200067932",
        "56106": "200067932",
        "56084": "200067932",
        "56087": "200067932",
        "56088": "200067932",
        }
