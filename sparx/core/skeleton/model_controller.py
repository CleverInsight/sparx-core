import os
import json
import uuid
import numpy as np
import pandas as pd
import tornado.web
from base_handler import base_handler
from sklearn.externals import joblib 



def convert_req_to_csv(fileinfo):
    ''' Get the batch file from request payload and convert to pandas dataframes

    Parameters:
    -----------
        fileinfo: Dict
            Enter a dictionary from payload which consist of filename, content
            body
    
    Usage:
    ------
        >>> convert_req_to_csv({filename: xyz, content: 'dsadsad'})
        >>> True
    '''
    # Actual filename
    extn = os.path.splitext(fileinfo['filename'])[1]

    random_filename = str(uuid.uuid4()) + extn

    # Generate file 
    temp_path = os.path.join(os.path.abspath(\
        os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", 'resources')), 'temp', random_filename)
    
    # Save batch test file
    with open(temp_path, 'w') as f:
        f.write(fileinfo['body'])
    
    return temp_path if os.path.exists(temp_path) else None





class controller_name(base_handler):

    def get(self):
        ''' start the basic API seletion '''
        data = dict(
            source='controllers/{}'.format('controller_name.py'),
            response=[]
        )
        self.write(json.dumps(data))
        self.finish()

    
    def post(self):
        ''' Create resources '''
        
        # Load the pickled model
        clf = joblib.load(os.path.join(os.path.abspath(\
            os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", 'resources')), 'models', 'controller_name.pkl'))

        # Save batch file into directory
        batch_path = convert_req_to_csv(self.request.files['batch'][0])

        # Read saved file using pandas dataframe
        x_test = pd.read_csv(batch_path)

        # Batch prediction    
        predicted = clf.predict(x_test.values)

        # Add predicted columns to given dataframe
        x_test.insert(loc=len(x_test.columns), column='predicted', value=predicted)
    
        # Response the given dataframe as JSON
        self.set_header('Content-Type', 'application/json')
        

        self.write(x_test.reset_index().to_json(orient='records'))
        self.finish()