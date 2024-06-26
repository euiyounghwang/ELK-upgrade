

# -*- coding: utf-8 -*-
import sys
import json

from elasticsearch import Elasticsearch
import argparse
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
from threading import Thread
from Search_Engine import Search
import logging
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def work(es_source_client, es_target_client, src_idx, dest_idx):
    ''' 
    The best way to reindex is to use Elasticsearch's builtin Reindex API as it is well supported and resilient to known issues.
    The Elasticsaerch Reindex API uses scroll and bulk indexing in batches , and allows for scripted transformation of data. 
    In Python, a similar routine could be developed:
    '''
    
    logging.info(f"{es_source_client, es_target_client, src_idx, dest_idx}")
    
    # scroll_time='60s'
    scroll_time='1m'
    batch_size='1000'
    total_progressing = 0
    
    es_obj_s = Search(host=es_source_client)
    es_client = es_obj_s.get_es_instance()
    
    es_obj_t = Search(host=es_target_client)
    es_t_client = es_obj_t.get_es_instance()
    
    body = {
        # "track_total_hits" : True,
        "query": { 
            "match_all" : {}
        }
    }

    rs = es_client.search(index=[src_idx],
        scroll=scroll_time,
        size=batch_size,
        body=body
    )

    # print(f'Current Size : {len(rs["hits"]["hits"])}')
    total_progressing += int(batch_size)
    logging.info(f'Ingest data .. : {str(total_progressing)}')
    
    ''' usu Search-Engine class '''
    es_obj_t.create_index(dest_idx)
    
    # es_obj_t.buffered_df_to_es(df=pd.DataFrame.from_dict(rs['hits']['hits']), _index=dest_idx)
    es_obj_t.buffered_json_to_es(raw_json=rs['hits']['hits'], _index=dest_idx)
    
    while True:
        # print(f'scroll : {rs["_scroll_id"]}')
        scroll_id = rs['_scroll_id']
        rs = es_client.scroll(scroll_id=scroll_id, scroll=scroll_time)
        if len(rs['hits']['hits']) > 0:
            # logging.info(rs['hits']['hits'])
            es_obj_t.buffered_json_to_es(raw_json=rs['hits']['hits'], _index=dest_idx)
            total_progressing += int(batch_size)
            logging.info(f'Ingest data .. : {str(total_progressing)}')
        else:
            break;
    
    '''
    curl -XPOST -u elastic:gsaadmin "http://localhost:9221/cp_test_omnisearch_v2/_search/?pretty" -H 'Content-Type: application/json' -d' {
        "track_total_hits" : true,
        "query": {
            "match_all": {
            }
        },
        "size" : 0
    }'
    
    '''    
    body = {
        "track_total_hits" : True,
        "query": { 
            "match_all" : {}
        }
    }


    es_t_client.indices.refresh(index=dest_idx)
    rs = es_t_client.search(index=[dest_idx],
        body=body
    )

    logging.info('-'*10)
    print(type(rs["hits"]["total"]), str(rs["hits"]["total"]))
    if isinstance(rs["hits"]["total"], int):
        logging.info(f'Validation Search Size : {rs["hits"]["total"]}')
    else:
        logging.info(f'Validation Search Size : {rs["hits"]["total"]["value"]}')
    logging.info('-'*10)


if __name__ == "__main__":
    
    '''
    (.venv) ➜  python-platform-engine git:(master) ✗ python ./Search-reindexing-script.py --es http://localhost:9200 --source_index test --ts https://localhost:9201
    '''
    parser = argparse.ArgumentParser(description="Index into Elasticsearch using this script")
    parser.add_argument('-e', '--es', dest='es', default="http://localhost:9209", help='host source')
    parser.add_argument('-t', '--ts', dest='ts', default="http://localhost:9292", help='host target')
    parser.add_argument('-s', '--source_index', dest='source_index', default="cp_recommendation_test", help='source_index')
    # parser.add_argument('-d', '--target_index', dest='target_index', default="test", help='target_index')
    args = parser.parse_args()
    
    if args.es:
        es_source_host = args.es
        
    if args.ts:
        es_target_host = args.ts
        
    if args.source_index:
        es_source_index = args.source_index

    '''
    if args.target_index:
        es_target_index = args.target_index
    else:
        es_target_index = args.source_index
    '''
    es_target_index = es_source_index
        
    # --
    # Only One process we can use due to 'Global Interpreter Lock'
    # 'Multiprocessing' is that we can use for running with multiple process
    # --
    try:
        th1 = Thread(target=work, args=(es_source_host, es_target_host, es_source_index, es_target_index))
        th1.start()
        th1.join()
        
    except Exception as e:
        logging.error(e)
        pass
    
  