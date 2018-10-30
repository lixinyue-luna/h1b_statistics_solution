import base

### PARAMS ###
K = 10  # find the top K elements
FIELDS = {  'occupations': ['SOC_NAME', 'LCA_CASE_SOC_NAME'],
            'states': ['WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE']}   # fields of interest
CONDITIONS = {'CERTIFIED': ['CASE_STATUS', 'STATUS']}   # dictionary of condition(s) {condition: [column_name(s)]}
INPUT_FILE  = 'h1b_input.csv'       # input filename
OUTPUT_FILE = 'top_K_COL-NAME.txt'  # output filename. must have the string 'K_COL-NAME'

### Main ###
# initialize an ApplicationData instance
newData = base.ApplicationData( fn_input = INPUT_FILE, 
                                fn_output = OUTPUT_FILE, 
                                fields = FIELDS,
                                conditions = CONDITIONS)

newData.readInput()     # read in and parse input data, store statistics in self.records
newData.topK(K)         # find K largest elements and write to output