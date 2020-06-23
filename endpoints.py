from flask import Flask, request
import json
import time
from utils import parse_xml, checkids, tup_to_dict


app = Flask(__name__)

@app.route('/ingest_and_check_byXpath', methods = ['POST'])
def run_check_ids():
    output, metrics, log, temp = {}, {}, {}, {}

    if request.method == 'POST':

        file = request.files['file']
        root = parse_xml(file)
        #check 1
        id_result = checkids(root)
        #check 2
        #check 3
        #...
        #check n

        if True in [boolean for (title, boolean) in id_result]:
            log['Components with duplicate ids'] = tup_to_dict(id_result, temp)
            log['time'] = time.strftime('%A %B, %d %Y %H:%M:%S')

        metrics['Components with duplicate ids'] = sum([boolean for (title, boolean) in id_result])

    metrics['total errors'] = sum(metrics.values())
    metrics['time'] = time.strftime('%A %B, %d %Y %H:%M:%S')

    output['XML_source'] = file.filename
    output['metrics'] = metrics
    output['log'] = log

    return json.dumps(output)

if __name__ == '__main__':
    app.run(debug=True)
