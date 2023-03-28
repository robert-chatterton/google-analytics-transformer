import json
from datetime import datetime
import uuid
import argparse

def gen_parse(filename: str):
    with open(filename) as open_file:
      line = open_file.readline()
      while line:
        yield json.loads(line)
        line = open_file.readline()
 
def transform_file(input: str, visits_output: str, hits_output: str) -> int:
  visits_output_file = open(visits_output, 'w')
  print(f'Visits outputting to `{visits_output}`')
  hits_output_file = open(hits_output, 'w')
  print(f'Hits outputting to `{hits_output}`')
  
  input_generator = gen_parse(input)
  line = next(input_generator)
  while line:
    visit_id = str(uuid.uuid4())
    visit = {
      'id': visit_id,
      'full_visitor_id': line['fullVisitorId'],
      'visit_id': line['visitId'],
      'visit_number': line['visitNumber'],
      'visit_start_time': datetime.fromtimestamp(int(line['visitStartTime'])).isoformat(),
      'browser': line['device']['browser'],
      'country': line['geoNetwork']['country']
    }
    
    hits = line['hits']
    hit_ids = []
    for hit in hits:
      hit_id = str(uuid.uuid4())
      output_hit = {
        'id': hit_id,
        'hit_number': hit['hitNumber'],
        'hit_type': hit['type'],
        'hit_timestamp': datetime.fromtimestamp(int(line['visitStartTime']) + int(hit['time'])).isoformat(),
        'page_path': hit['page']['pagePath'],
        'page_title': hit['page']['pageTitle'],
        'hostname': hit['page']['hostname']
      }
      hit_ids.append(hit_id)
      hits_output_file.write(f'{json.dumps(output_hit)}\n')

    visit['hits'] = hit_ids
    visits_output_file.write(f'{json.dumps(visit)}\n')
    
    try:
      line = next(input_generator)
    except StopIteration:
      break
  
  visits_output_file.close()
  hits_output_file.close()
  print(f'Parsed `{input}`')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog='Google Analytics Transformer - Housecall Pro Data Engineering Test')
  parser.add_argument('filename')
  parser.add_argument('--visits', help='output file for visit data')
  parser.add_argument('--hits', help='output file for hit data')
  args = parser.parse_args()

  if (args.visits == None):
    visits = 'visits.json'
  else:
    visits = args.visits
    
  if (args.hits == None):
    hits = 'hits.json'
  else:
    hits = args.hits

  transform_file(args.filename, visits_output=visits, hits_output=hits)
