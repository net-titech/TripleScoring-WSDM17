#!/home/hoangnt/anaconda3/bin/python

# Author: Hoang NT
# Date: 2016/10/11
# Get data from Google Knowledge Graph

import json
import urllib
import urllib.request as request
import urllib.parse as parse
import argparse as ap
from os import path

parser = ap.ArgumentParser(description='Get person ranking from GGK.')
parser.add_argument('--input', nargs=1, type=str, 
                    help='Name-id file location.')
parser.add_argument('--output', nargs=1, type=str,
                    help='Output file contains Name-id-score.')
args = parser.parse_args()

def freebase_to_gk(ids):
    return '/' + ids.replace('.','/')

def main():
    input_loc = args.input[0]
    assert path.exists(input_loc), 'Input file not found.'
    output_loc = args.output[0]
    api_key = open('.knowledge_graph_api_key').read()
    params = {
        'indent': True,
        'key': api_key,
        'ids': '',
    }
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search?'
    with open(input_loc, 'r') as ifile:
        with open(output_loc, 'w') as ofile:
            for line in ifile.readlines():
                name, ids = line.strip().split('\t')
                params['ids'] = freebase_to_gk(ids)
                url = service_url + parse.urlencode(params)
                print(url)
                try:
                    with request.urlopen(url) as response:
                        data = json.loads(response.read().decode('utf8'))
                except:
                    print('Skipping...' + url)
                    continue
                try: 
                    info = data['itemListElement'][0]
                except:
                    print('Skipping empty data...' + url) 
                    continue
                score = info['resultScore']
                string = name + '\t' + ids + '\t' + str(score) + '\n'
                ofile.write(string)

if __name__ == '__main__':
    main()
