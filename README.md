# Sarswati Data Quality

The purpose of this package is to create automated data quality checks against C-CDA files.

There is currently one endpoint that ingests and runs a check for unique ids per component within the C-CDA.

Requirements:
* Python 3.0+

Setup:
* run `pip install -r requirements` 


Test the Script:
* run `python endpoints.py`
* Open postman and hit the endpoint with
    * form-data:
    
        *`Key`: `"file"` (NOTE: make sure the "file" drop down is selected)
        
        *`Value`: `{upload C-CDA file}`
        
        *`Content Type`: `"multipart/form-data"`
        
    * expected return: JSON containing Titles of components and "No duplicates" or "Duplicates are present"
