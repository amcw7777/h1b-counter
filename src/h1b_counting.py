import sys
from preprocess import Preprocessor
from data_analyze import H1BCounter
'''
A macro to run Preprocessor and H1BCounter for H1B statistic analysis

Author and Mainainer:
    Liang He (liangheNOSPAM@gmail.com)
'''


def preprocess():
    '''
    call preprocessor to process raw data
    '''
    preprocessor = Preprocessor()
    preprocessor.preprocess(input_file_name)

def data_analyze():
    '''
    call analyzer to analyze the processed data
    '''
    analyzer = H1BCounter(input_file_name, output_occupation_name, output_state_name)
    analyzer.analyze()

if __name__ == "__main__":
    '''
    @argv[1]: input file name
    @argv[2]: top_10_occupations output
    @argv[3]: top_10_states output
    '''
    if len(sys.argv) < 4:
        print "Usage: python ./src/h1b_counting.py \
                ./input/h1b_input.csv \
                ./output/top_10_occupations.txt \
                ./output/top_10_states.txt"
    input_file_name = sys.argv[1]
    output_occupation_name = sys.argv[2]
    output_state_name = sys.argv[3]
    preprocess()
    data_analyze()


