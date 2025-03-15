import requests


def get_ha_sensor(access_token, host, sensor_name):
    r = requests.get(f'https://{host}/api/states/{sensor_name}', headers={'Authorization': f'Bearer {access_token}'})
    j = r.json()
    return j['state'], j['attributes']['unit_of_measurement']
