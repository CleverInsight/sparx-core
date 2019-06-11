import os
import json
import uuid
import numpy as np
import pandas as pd
import tornado.web
from base_handler import base_handler
from sklearn.externals import joblib 



def convert_req_to_csv(fileinfo):
    ''' Get the batch file from request payload and convert to pandas 
    dataframes
    '''
    fname = fileinfo['filename']

    # Actual filename
    extn = os.path.splitext(fname)[1]

    # # New filename
    cname = str(uuid.uuid4()) + extn
    fh = open('temp.csv', 'w') 
    fh.write(fileinfo['body'])





class iris_controller(base_handler):

    def get(self):
        ''' start the basic API seletion '''
        data = dict(
            source='controllers/{}'.format('iris_controller.py'),
            response=[]
        )
        self.write(json.dumps(data))
        self.finish()

    
    def post(self):
        ''' Create resources '''
        
        # Load the pickled model
        clf = joblib.load(os.path.join(os.path.abspath(\
            os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", 'resources')), 'models', 'iris_controller.pkl'))

        fileinfo = self.request.files['batch'][0]

        # Actual filename
        extn = os.path.splitext(fileinfo['filename'])[1]

        random_filename = str(uuid.uuid4()) + extn

        # Generate file 
        temp_path = os.path.join(os.path.abspath(\
            os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", 'resources')), 'temp', random_filename)
        
        # Save batch test file
        with open(temp_path, 'w') as f:
            f.write(fileinfo['body'])

        # Read saved file using pandas dataframe
        x_test = pd.read_csv(temp_path)

        # Batch prediction    
        predicted = clf.predict(x_test.values)

        # Add predicted columns to given dataframe
        x_test.insert(loc=len(x_test.columns), column='predicted', value=predicted)
    
        # Response the given dataframe as JSON
        self.set_header('Content-Type', 'application/json')
        
        self.write(x_test.reset_index().to_json(orient='records'))
        self.finish()

