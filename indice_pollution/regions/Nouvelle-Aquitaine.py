from dateutil.parser import parse
from datetime import timedelta
from . import ForecastMixin

class Forecast(ForecastMixin):
    url = 'https://opendata.atmo-na.org/geoserver/ind_nouvelle_aquitaine_agglo/wfs'

    @classmethod
    def insee_list(cls):
        return ['33063', '79005', '16102', '64102', '64445', '19272', '87085',
            '24322', '40088', '17300', '16015', '79191', '87154', '86194', '19031',
            '64300', '23096'
        ]

    @classmethod
    def params(cls, date, insee):
        tomorrow = (parse(date) + timedelta(hours=24)).date()

        filter_zone = f'<PropertyIsEqualTo><PropertyName>code_zone</PropertyName><Literal>{insee}</Literal></PropertyIsEqualTo>'
        filter_date = f'<PropertyIsGreaterThanOrEqualTo><PropertyName>date_ech</PropertyName><Function name="dateParse"><Literal>yyyy-MM-dd</Literal><Literal>{date}</Literal></Function></PropertyIsGreaterThanOrEqualTo>'

        return {
            'request': 'GetFeature',
            'service': 'WFS',
            'version': '1.1',
            'typeName': 'ind_nouvelle_aquitaine_agglo:ind_nouvelle_aquitaine_agglo',
            'Filter': f"<Filter><And>{filter_zone}{filter_date}</And></Filter>",
            'outputFormat': 'json',
        }

    @classmethod
    def getter(cls, feature):
        return {
            **{
                'indice': feature['properties']['valeur'],
                'date': str(parse(feature['properties']['date_ech']).date())
            },
            **{k: feature['properties'][k] for k in cls.outfields if k in feature['properties']}
        }