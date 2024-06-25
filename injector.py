
from config.log_config import create_log
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import json
import os


def get_headers():
    ''' Elasticsearch Header '''
    return {'Content-type': 'application/json', 'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')), 'Connection': 'close'}


load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


es_client = Elasticsearch(hosts=os.getenv("ES_HOST"),
                          headers=get_headers(),
                          verify_certs=False,
                          timeout=5
)
