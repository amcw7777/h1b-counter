import sys
import re
import h1b_tools as tools
from states import state_map
from states import zip_list 

class Preprocessor(object):
    '''
    Preprocess H1B row data
    Clean and keep the 'state', 'soc_code', 'soc_name' informations for certified cases

    @input: h1b raw data
    @output1: processed data with colums 'state', 'soc_code', 'soc_name'
    @output2: counting of cases with certain soc_code and soc_name

    Usage:
        from preprocess import Preprocessor
        processor = Preprocessor()
        processor.preprocess(input_name)

    Author and Mainainer:
        Liang He (liangheNOSPAM@gmail.com)
    '''
    def __init__(self):
        self.output_file = None
        self._total_counter = 0
        self.soc_code_map_counter = {}
        self.soc_code_map = {}

    def preprocess(self, input_file_name):
        '''
        clean and slim the input data
        @output: state, occupation
        @type input_file_name: string
        @rtype: nothing
        '''
        print 'Start process', input_file_name, '...'
        file_name = input_file_name.split('/')[-1]
        self.output_file = open('./src/processed_'+file_name, 'w')
        self.output_file.write('STATE;SOC_CODE;SOC_NAME\n')
        with open(input_file_name) as file:
            status_idx, state_idx, soc_code_idx, soc_name_idx = None, None, None, None
            for line in file:
                cols = re.split(r';(?=([^\"]*\"[^\"]*\")*[^\"]*$)', line)
                # cols = tools.split(line, ';')
                '''
                the regular expression is to deal with cases like "xxx;xxxx"
                '''
                if self._total_counter == 0:
                    '''
                    the first line to locate the indices for status, state, tilte and code
                    '''
                    for i, col in enumerate(cols):
                        if not col:
                            continue
                        if 'STATE' in col and 'WORK' in col and not state_idx:
                            state_idx = i
                        if 'STATUS' in col and not status_idx:
                            status_idx = i
                        if 'NAME' in col and 'SOC' in col and not soc_name_idx:
                            soc_name_idx = i
                        if 'CODE' in col and 'SOC' in col and not soc_code_idx:
                            soc_code_idx = i
                    self._total_counter += 1
                else:
                    status = cols[status_idx].strip().upper()
                    if cols[status_idx] != 'CERTIFIED':
                        continue
                    soc_code = tools.clean_soc_code(cols[soc_code_idx])
                    soc_name = tools.clean_soc_name(cols[soc_name_idx])
                    state = (cols[state_idx]).strip('"')
                    if state not in state_map or not state:
                        zip_code = (cols[state_idx+2]).strip('"')
                        state = self.get_state_from_zip(int(zip_code))
                    self.output_file.write('"'+state+'";"'+soc_code+'";"'+soc_name+'"\n')
                    self.build_dict(soc_name, soc_code) # count soc_name, soc_code
                    self._total_counter += 1
                if self._total_counter % 100000 == 0:
                    print self._total_counter, 'cases processed...'
        print self._total_counter, 'certified cases processed'
        self.print_soc_code_map(file_name)
        self.output_file.close()

    def build_dict(self, name, code):
        '''
        update soc_code_map_counter based on name and code
        @type name: string
        @type code: string
        @rtype: nothing
        '''
        # if not name:
        #     return
        if code not in self.soc_code_map_counter:
            self.soc_code_map_counter[code] = {}
        if name not in self.soc_code_map_counter[code]:
            self.soc_code_map_counter[code][name] = 0
        self.soc_code_map_counter[code][name] += 1

    def print_soc_code_map(self, file_name):
        '''
        write the soc_code_map into file
        @type file_name: string
        @rtype: nothing
        '''
        output_map = open('./src/soc_map_'+file_name, 'w')
        for code in self.soc_code_map_counter:
            for name in self.soc_code_map_counter[code]:
                counting = str(self.soc_code_map_counter[code][name])
                output_map.write(code+';"'+name+'";'+counting+'\n')
        output_map.close()

    def get_state_from_zip(self, zip_code):
        '''
        get state from zip code
        @type zip_code: integer
        @rtype: string
        '''
        for zip_map in zip_list:
            for zip_range in zip_map[1:]:
                if ',' not in zip_range:
                    if zip_code == int(zip_range):
                        return zip_map[0]
                else:
                    zip_low, zip_high = zip_range.split(',')
                    if int(zip_low) <= zip_code <= int(zip_high):
                        return zip_map[0]
        return '?'
