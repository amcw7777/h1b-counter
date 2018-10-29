import sys
import re
from occupation_checker import OccupationChecker
import h1b_tools as tools

class H1BCounter(object):
    '''
    Analyze the processed H1B processed data.
    Calculate 1)top 10 Occupations and 2)top 10 States for certified visa applications.

    @input1: preprocess_data, with columns: state; soc_code; soc_name
    @input2: counting of soc_code, soc_name
    @output1: top 10 Occupations, the counting and the percentage
    @output2: top 10 States, the counting and the percentage

    Usage:
        from data_analyze import H1BCounter
        counter = H1BCounter(input_name, output1_name, output2_name)
        counter.analyze()

    Author and Mainainer:
        Liang He (liangheNOSPAM@gmail.com)
    '''
    def __init__(self, input, output1, output2):
        self.state_counter = {}
        self.occupation_counter = {}
        self.total_counter = 0

        self.input_file_name = input.split('/')[-1]
        self.output_occupation_name = output1
        self.output_state_name = output2

        self.soc_code_map = {}
        self.occupation_dict = set()

    def analyze(self):
        '''
        count the number of occupations and states from processed data
        '''
        self.load_soc_map()
        processed_file = './src/processed_'+self.input_file_name
        checklist = {}
        with open(processed_file) as file:
            next(file)
            for line in file:
                cols = re.split(r';(?=([^\"]*\"[^\"]*\")*[^\"]*$)', line)
                '''
                the regular expression is for case "xxx;xxxx"
                '''
                state = cols[0].strip('"')
                code = cols[2].strip('"')
                name = cols[4].strip('"\n')

                if state not in self.state_counter:
                    self.state_counter[state] = 0
                self.state_counter[state] += 1

                occupation = self.get_occupation(code, name)

                if occupation not in self.occupation_counter:
                    self.occupation_counter[occupation] = 0
                self.occupation_counter[occupation] += 1
                self.total_counter += 1
        self.print_result()

    def load_soc_map(self):
        '''
        load soc_code - soc_name - counting map from precessed file
        '''
        map_file = './src/soc_map_'+self.input_file_name
        soc_code_counter = {}
        with open(map_file) as file:
            for line in file:
                cols = re.split(r';(?=([^\"]*\"[^\"]*\")*[^\"]*$)', line)
                code, name, count = cols[0], cols[2].strip('"'), int(cols[4])
                if code not in soc_code_counter:
                    soc_code_counter[code] = {}
                soc_code_counter[code][name] = count
        self.vote_code_map(soc_code_counter)

    def vote_code_map(self, counter):
        '''
        choose the soc_name with most counting corresponding the soc_code
        save the valid soc_name into occupation_dict
        '''
        for code in counter:
            temp_list = []
            for name in counter[code]:
                temp_list.append([counter[code][name], name])
            temp_list.sort(reverse=True)
            self.soc_code_map[code] = temp_list[0][1]
            if len(re.findall(r'\d+', temp_list[0][1])) == 0:
                self.occupation_dict.add(temp_list[0][1])


    def get_occupation(self, code, name):
        '''
        if name in occupation dict, return the name
        else find the name based on soc_code
        '''
        if name in self.occupation_dict:
            return name
        return self.soc_code_map[code]


    def print_result(self):
        '''
        print top10 results to the ouput files
        '''
        def compare(item1, item2):
            '''
            sort by decreasing counting
            in case of a tie, sort alphabetically
            '''
            if item1[1] != item2[1]:
                return item2[1] - item1[1]
            else:
                if item1[0] < item2[0]:
                    return -1
                else:
                    return 1

        state_list = []
        for state in self.state_counter:
            state_list.append((state, self.state_counter[state]))
        state_list.sort(cmp=compare)
        output_state = open(self.output_state_name, 'w')
        output_state.write('TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for i in range(min(10, len(state_list))):
            percentage = str(round(1.0*state_list[i][1]*100/self.total_counter, 1)) + '%'
            output_state.write(state_list[i][0]+';'+\
                                    str(state_list[i][1])+\
                                    ';'+percentage+'\n')
        output_state.close()
        occupation_list = []
        for occupation in self.occupation_counter:
            occupation_list.append((occupation, self.occupation_counter[occupation]))
        occupation_list.sort(cmp=compare)
        output_occupation = open(self.output_occupation_name, 'w')
        output_occupation.write('TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n')
        for i in range(min(10, len(occupation_list))):
            percentage = str(round(1.0*occupation_list[i][1]*100/self.total_counter, 1)) + '%'
            output_occupation.write(occupation_list[i][0]+';'+\
                                    str(occupation_list[i][1])+\
                                    ';'+percentage+'\n')
        output_occupation.close()
