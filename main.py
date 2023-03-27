import json
from datetime import datetime
import uuid

def gen_parse(filename: str):
    with open(filename) as open_file:
      line = open_file.readline()
      while line:
        yield json.loads(line)
        line = open_file.readline()
 
def transform_file(input: str, visits_output: str = 'visits.json', hits_output: str = 'hits.json') -> int:
  visits_output_file = open(visits_output, 'w')
  hits_output_file = open(hits_output, 'w')
  
  input_generator = gen_parse(input)
  line = next(input_generator)
  while line:
    visit = {
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
  return 0

if __name__ == '__main__':
  transform_file('ga_sessions_20160801_(2)_(1)_(1)_(1).json')
