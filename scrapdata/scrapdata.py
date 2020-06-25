import pyowm
from pyowm.utils.geo import Polygon as GeoPolygon
from pyowm.agroapi10.enums import SatelliteEnum, PresetEnum
from pyowm.commons.enums import ImageTypeEnum
from pyowm.agroapi10.enums import PaletteEnum
import requests


class Scrap:
    def __init__(self, places):
        self.APIkey = "32ce3717017406682b290a5dd99fbc99"
        self.polygonID = "5ec171ae5214af4bd1ddbd9c"
        self.token_air_pollution = "8870b6555dbf1ac8c1f5010ee1556582bac1f000"
        self.token_stormglass = "d8d2fd56-986c-11ea-aa6d-0242ac130002-d8d2fe14-986c-11ea-aa6d-0242ac130002"
        self.places = places
        self.data_dict = dict()
        self.owm = pyowm.OWM(self.APIkey)  # You MUST provide a valid API key
        self.gp = GeoPolygon([[[-1.865616, 43.296621], [-1.865624, 43.294515], [-1.862518, 43.29459], [-1.861085, 43.295477],
                          [-1.859961, 43.295277], [-1.860922, 43.296446], [-1.861488, 43.296627],
                          [-1.865616, 43.296621]]])
        self.mgr = (self.owm.agro_manager())
        self.data = []

    def get_wheather_data(self):
        for place in self.places:
            observation = self.owm.weather_at_place(place)
            print(observation.to_JSON())
            w = observation.get_weather()
            self.data_dict = dict(place=place,
                                  sunrise=w.get_sunrise_time('iso'),
                                 sunset=w.get_sunset_time('iso'),
                                 status=w.get_detailed_status(),
                                 temperature=w.get_temperature('celsius')['temp'],
                                  temperature_max=w.get_temperature('celsius')['temp_max'],
                                  temperature_min=w.get_temperature('celsius')['temp_min'],
                                 humidity= w.get_humidity(),
                                 wind_speed=w.get_wind()['speed'],
                                 wind_deg=w.get_wind()['deg'],
                                  #ico=w.get_wheather_icon_name(),
                                 time=w.get_reference_time(timeformat='date'))
            self.data.append(self.data_dict)
        return self.data

    def get_agro_data(self):
        polygon_oiartzun = self.mgr.create_polygon(self.gp, 'Oiartzun')
        soil = self.mgr.soil_data(polygon_oiartzun)
        agro_data = dict(moisture=soil.moisture,
                         surface_temp=soil.surface_temp(unit='celsius'),
                         ten_cm_temp=soil.ten_cm_temp(unit='celsius'))
        print(agro_data)

    def get_satellite_data(self):
        pol_id = self.polygonID  # your polygon's ID
        acq_from = 1500336000  # 18 July 2017
        acq_to = 1508976000  # 26 October 2017
        img_type = ImageTypeEnum.GEOTIFF  # the image format type
        preset = PresetEnum.NDVI  # the preset
        sat = SatelliteEnum.LANDSAT_8.symbol  # the satellite
        metaimages_list = self.mgr.search_satellite_imagery(pol_id, acq_from, acq_to)
        print(metaimages_list[0])
        bnw_sat_image = self.mgr.download_satellite_image(metaimages_list[0])
        stats_dict = self.mgr.stats_for_satellite_image(bnw_sat_image)
        print(stats_dict)

        # results = self.mgr.search_satellite_imagery(pol_id, acq_from, acq_to, img_type=img_type, preset=preset, None, None,
        #                                        acquired_by=sat)
        #
        # satellite_images = [self.mgr.download_satellite_image(result) for result in results]
        # sat_img = satellite_images[0]
        # stats_dict = self.mgr.stats_for_satellite_image(sat_img)
        # sat_img.persist('/path/to/my/folder/sat_img.tif')

    def get_airpollution_data(self):
        data = []
        for place in self.places:
            url = "http://api.waqi.info/feed/donosti/?token={}".format(self.token_air_pollution)
            result = requests.get(url=url).json()['data']['iaqi']
            pollution_data = dict(city=place,
                                  co=result['co']['v'],
                                  h=result['h']['v'],
                                  no2=result['no2']['v'],
                                  o3=result['o3']['v'],
                                  p=result['p']['v'],
                                  pm10=result['pm10']['v'],
                                  pm25=result['pm25']['v'],
                                  so2=result['so2']['v'],
                                  t=result['t']['v'],
                                  w=result['w']['v'],
                                  wg=result['wg']['v'])
            data.append(pollution_data)
            print(pollution_data)

    def get_ocean_data(self):
        # 'https://api.stormglass.io/v1/tide/extremes/point',

        response = requests.get(
            'https://api.stormglass.io/v1/weather/point',
            params={'lat': 58.5,'lng': 17.8},
            headers={'Authorization': self.token_stormglass})
        json_data = response.json()
        print(json_data)

    def __del__(self):
        print('Destructor {}'.format(self.__class__))

w = Scrap(['San Sebastian, ES', 'Oiartzun, ES'])
w.get_ocean_data()



