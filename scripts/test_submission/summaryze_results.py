import json
import pandas
import os
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

result_filepaths = sorted(glob.glob(os.path.join(SCRIPT_DIR, 'results', '*.json')))
results = []
for result_filepath in result_filepaths:
    with open(result_filepath, 'r') as f:
        data = json.load(f)
        data['name'] = os.path.splitext(os.path.basename(result_filepath))[0]
        results.append(data)

df = pandas.DataFrame(results)
df.set_index('name', inplace=True)
df = df.round(4)
df.to_csv(os.path.join(SCRIPT_DIR, 'summary.csv'))
