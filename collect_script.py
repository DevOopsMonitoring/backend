import requests
from time import sleep
from json import loads, dumps
import subprocess


URL = 'https://devoops.w0rng.ru'
GET_RULES_URL = '/api/v1/rule/'
SEND_DATA_URL = '/api/v1/data/'
TOKEN = '{TOKEN}'


def get_data(snmp: str) -> str:
    command = 'snmpget -u bootstrap -l authPriv -a MD5 -x DES -A hard_password -X hard_password localhost ' + snmp
    data = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    return data.split(':')[-1].strip()


def send_data(data: dict):
    requests.post(URL+SEND_DATA_URL+TOKEN, json=data)


def get_snmp():
    data = requests.get(URL+GET_RULES_URL+TOKEN).text
    data = loads(data)
    for code in data.get('rules'):
        data = get_data(code['snmp'])
        tmp = dict()
        tmp['sensor_id'] = code['sensor_id']
        tmp['value'] = data
        send_data(tmp)

if __name__ == '__main__':
    while True:
        get_snmp()
        sleep(60)
