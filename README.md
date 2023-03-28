# Google Analytics Transformer

Housecall Pro Data Engineering Take Home Exercise

Robert Chatterton
Developed with Python 3.9.7

`python transform.py <filename>` outputs by default to `visits.json` and `hits.json`.

### Sample

For the sample file, unzip `ga_sessions_20160801.json.gz` to `ga_sessions_20160801.json`.

Run `python transform.py ga_sessions_20160801.json`

### Optional Arguments

- `--visits` changes the output file for visit data
- `--hits` changes the output file for hit data
