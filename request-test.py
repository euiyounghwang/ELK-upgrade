
import requests
from requests.auth import HTTPBasicAuth
import json
from elasticsearch import Elasticsearch, exceptions
import os 
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")


''' pip install python-dotenv'''
load_dotenv() # will search for .env file in local folder and load variables 


def elasticsearch_es():
    '''
    $ python ./request-test.py
    {
    "name": "test-es8-node#1",
    "cluster_name": "test-es8-node#1-es8-dev",
    "cluster_uuid": "Rs0Ec26mQSK83RIo52il5g",
    "version": {
        "number": "8.12.2",
        "build_flavor": "default",
        "build_type": "tar",
        "build_hash": "48a287ab9497e852de30327444b0809e55d46466",
        "build_date": "2024-02-19T10:04:32.774273190Z",
        "build_snapshot": false,
        "lucene_version": "9.9.2",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "You Know, for Search"
    }
    '''
    header =  {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
    }
    es_client = Elasticsearch(hosts=os.getenv("ES_HOST"),
                              headers=header,
                            #   http_auth=('test', 'test'),
                              verify_certs=False,
                              max_retries=0,
                              timeout=5)
    print(json.dumps(es_client.cluster.health(), indent=2))
    


def request_es():
    '''
    $ python ./request-test.py
    {
    "name": "test-es8-node#1",
    "cluster_name": "test-es8-node#1-es8-dev",
    "cluster_uuid": "Rs0Ec26mQSK83RIo52il5g",
    "version": {
        "number": "8.12.2",
        "build_flavor": "default",
        "build_type": "tar",
        "build_hash": "48a287ab9497e852de30327444b0809e55d46466",
        "build_date": "2024-02-19T10:04:32.774273190Z",
        "build_snapshot": false,
        "lucene_version": "9.9.2",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "You Know, for Search"
    }

    '''
    header =  {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
    }
    # res = requests.get(url=host, auth=HTTPBasicAuth("test", "test"), verify=False)
    res = requests.get(url=os.getenv("ES_HOST"), headers=header, verify=False)
    print(json.dumps(res.json(), indent=2))


if __name__ == '__main__':
    '''  Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings '''
    print('\n*****')
    request_es()
    print('\n*****')
    elasticsearch_es()