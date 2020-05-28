from flask import Flask, request
import pandas as pd
import json
import checks
from utils import find_nested_indexes, get_components, flatten_dict, flatten_dict_detailed, CCDAIngest_fromstring

app = Flask(__name__)

#TODO: remove check functionality from this endpoint
#TODO: make this endpoint just upload + parse C-CDA

@app.route('/ingest_and_check', methods = ['POST'])
def ingest_and_parse_components():
    duplicated = []

    if request.method == 'POST':

        file = request.files['file']
        df = CCDAIngest_fromstring(file.read())
        components = pd.DataFrame(get_components(df, find_nested_indexes(df)))

        for x in components['section']:
            this_df = pd.DataFrame(flatten_dict_detailed(flatten_dict(x)).items(), columns=['tag', 'value'])
            duplicated.append(checks.check_duplicates_ids(this_df))

    return json.dumps(dict(duplicated))

#TODO: create seperate endpoint for each check
@app.route('/check_duplicate_ids', methods = ['GET'])
def check_duplicate_ids(components):
    duplicated = []

    for x in components['section']:
        this_df = pd.DataFrame(flatten_dict_detailed(flatten_dict(x)).items(), columns=['tag', 'value'])
        duplicated.append(checks.check_duplicates_ids(this_df))

    return json.dumps(dict(duplicated))

if __name__ == '__main__':
    app.run(debug=True)
