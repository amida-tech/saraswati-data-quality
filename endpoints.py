from flask import Flask, request
import pandas as pd
import json
import checks
from utils import find_nested_indexes, get_components, CCDAIngest_fromstring, parse_xml, checkids


app = Flask(__name__)

@app.route('/ingest_and_check', methods = ['POST'])
def ingest_and_run_checks():
    """
    This end point allows user to POST an CCDA XML file and will return
    a check on the unique id's per component.

    :return: tuple containing boolean that denotes if there are duplicates in a particular
             component, and the title of that component
    :rtype: tuple(boolean, str)
    """
    flags = []

    if request.method == 'POST':

        file = request.files['file']
        df = CCDAIngest_fromstring(file.read())
        components = pd.DataFrame(get_components(df, find_nested_indexes(df)))

        checks.unique_ids(components, flags)

        #continue to add more checks here

    return json.dumps(dict(flags))

@app.route('/ingest_and_check_byXpath', methods = ['POST'])
def run_check_ids():
    output, metrics, log = {}, {}, {}

    if request.method == 'POST':

        file = request.files['file']
        root = parse_xml(file)
        id_result = checkids(root)

        if True in [boolean for (title, boolean) in id_result]:
            log['duplicate_ids'] = id_result


    metrics['Duplicate Ids count'] = sum([boolean for (title, boolean) in id_result])

    output['metrics'] = metrics
    output['log'] = log

    return json.dumps(output)

if __name__ == '__main__':
    app.run(debug=True)
