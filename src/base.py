# This Python file uses the following encoding: utf-8
'''
A library to support H1B Statistics Project
'''
import sys
import os
import csv
import heapq

### PARAMS ###
# Folder directories
ROOT_DIR    =   os.path.dirname(os.path.dirname(__file__))        # get parent directory of file
SRC_DIR     =   os.path.join(ROOT_DIR, 'src')       # get directory of src folder
INPUT_DIR   =   os.path.join(ROOT_DIR, 'input')     # get directory of input folder
OUTPUT_DIR  =   os.path.join(ROOT_DIR, 'output')    # get directory of output folder
DIRs        =   {   'src'   :   SRC_DIR,
                    'input' :   INPUT_DIR, 
                    'output':   OUTPUT_DIR  }       # dictionary of folder directories

### DEFINE FUNCTIONS ###
def get_filepath(fileType = '', filename = ''):
    '''
    Construct and return file path.

    :param str fileType: Type of the file in this project, e.g. 'input' for input files, 'output' for output files
    :param str filename: Filename to append to folder path
    :return: filepath
    :rtype: str
    '''
    try:
        folder_path = DIRs[fileType]    # get folder directory
    except:
        raise KeyError('Invalid file type {}'.format(fileType)) # raise KeyError if fileType is not defined in DIRs.
    return os.path.join(folder_path, filename)

### CLASS DEFINITION ###
class ApplicationData(object):
    ''' 
    Class representing visa application data
    '''
    def __init__(self, fn_input, fn_output, fields, conditions, **kargs):  
        '''
        :param str fn_input:    name of input file
        :param str fn_output:   name of output file
        :param dict fields:     dictionary of fields of interests {field: [column_name(s)]} i.e. {'occupations': ['SOC_NAME', 'LCA_CASE_SOC_NAME']}
        :param conditions:      dictionary of condition(s) {condition: [column_name(s)]} i.e. {'CERTIFIED': ['CASE_STATUS', 'STATUS']}
        '''
        self.fn_input   =   get_filepath(fileType = 'input', filename = fn_input)  
        self.fn_output  =   get_filepath(fileType = 'output', filename = fn_output)
        self.fields     =   fields   
        self.conditions =   conditions
        
        # dictionary of records of interest. default is empty dict. 
        # i.e. {'occupations':{SOC_CODE:frequency}, {'states':{state:frequency}}}
        self.records    =   {}       
        for key in self.fields:
            self.records.setdefault(key, {})    
        
        # count total number of cases that meet condition. 
        self.counter    =   0     
        
        # dictionary to store sorted data. i.e. {'occupations':[], 'states':[]}
        self.result     =   {}      

        # header of output file
        self.res_header =   ['TOP_FEATURE','NUMBER_CERTIFIED_APPLICATIONS','PERCENTAGE']    

    def readInput(self):
        '''
        Read in and parse input csv data line by line. Store frequencies of fields of interest as dictionaries.
        '''
        with open(self.fn_input) as f:
            fh      =   csv.reader(f, delimiter=';')   # csv file handler
            header  =   fh.next()   # get header row
            
            # dictionary to keep positions of columns of conditions. i.e. {'CERTIFIED': 2}
            condition_pos = {}  
            for key in self.conditions:
                # column names can differ in different years. 
                for col_name in self.conditions[key]:
                    try:
                        condition_pos[key] = header.index(col_name)
                        break
                    except ValueError:
                        pass
            
            # dictionary to keep positions of columns of interest. i.e. {'states': 50, 'occupations': 24}
            field_pos   =   {}          
            for key in self.fields:
                # column names can differ in different years
                for col_name in self.fields[key]:
                    try:
                        field_pos[key] = header.index(col_name)
                        break
                    except ValueError:
                        pass
            
            # iterate over file handler and parse data
            for row in fh:
                # skip cases that do not meet all conditions
                flag = True
                for key in self.conditions:
                    if row[condition_pos[key]] != key:
                        flag = False
                        break
                # if a case meets all conditions, add case to records, otherwise continue to next interation
                if flag:
                    self.counter += 1
                    for i in self.fields:
                        self.records[i][row[field_pos[i]]] = self.records[i].setdefault(row[field_pos[i]], 0) + 1
                else:
                    continue
    
    def writeOutput(self, K, feature, values):
        '''
        Write sorted result to output files.

        :param int K: K results.
        :param str feature: e.g. 'occupations', 'states'
        :param list values: a list of lists of values. e.g. [('SOFTWARE DEVELOPERS, APPLICATIONS', 6)]
        '''
        filepath = self.fn_output.replace('K', str(K)).replace('COL-NAME', feature)
        header = ';'.join(self.res_header).replace('FEATURE', feature.upper())

        with open(filepath, 'w') as fh:
            fh.write(header)
            for v in values:
                fh.write('\n{name};{count};{percentage:.1f}%'.format(name = v[0], count = v[1], percentage = round(v[1]*100.0/self.counter, 1)))
    
    def heapSortLargest(self, K, fieldDict): 
        '''
        Sort by value and then by key. Return a list of (key, value) pairs. e.g. (state name, count)
        :param dict fieldDicts: a record dictionary. format: {field_name: count}
        :return: sorted list of (key, value) tuples ordered by (value, key)
        :rtype: list
        '''
        # First sorted by frequency (largest to smallest), then by field name (A to Z)
        return heapq.nsmallest(K, fieldDict.items(), key = lambda p: (-p[1], p[0]))
        
    def topK(self, K, features = None):
        '''
        Find top K frequent values.

        :param int K: number of records wanted in each category
        :param list feature: list of features of interest. default is all features specified in fields. e.g. ['occupations', 'states']
        '''
        if not features: 
            features = self.fields.keys()
        
        for feature in features:
            self.result[feature] = self.heapSortLargest(K, self.records[feature])
            self.writeOutput(K, feature, self.result[feature])