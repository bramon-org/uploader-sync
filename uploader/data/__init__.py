import os

BASE_PATH = os.path.dirname(__file__)
# API_URL = 'http://local-api.bramonmeteor.org/v1/operator/captures'
API_URL = 'https://api.bramonmeteor.org/v1/admin/captures'
API_TOKEN = os.environ.get('API_TOKEN')
STATIONS_MAP = "{}/../data/stations.json".format(BASE_PATH)
