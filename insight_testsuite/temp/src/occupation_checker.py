import re
import h1b_tools as tools

class OccupationChecker(object):
    def __init__(self):
        self.soc_code_map_file = {}
        self.occupation_dict = set()

        self.build_dict_from_file()

    def get_occupation(self, code, name):
        '''
        get occupation title from soc_name and soc_code
        @type name: string
        @type code: string
        @rtype: string
        '''
        if name in self.occupation_dict:
            # the name is a valid occupation title
            if code not in self.soc_code_map_file: # update code_map
                self.soc_code_map_file[code] = name
            return name
        if code in self.soc_code_map_file:
            # wrong name but correct soc_code
            return self.soc_code_map_file[code]
        if len(code) == 7 and code+'.00' in self.soc_code_map_file:
            # xx-xxxx.00 for xx-xxxx
            return self.soc_code_map_file[code+'.00']
        if len(code) == 10 and code[:7]  in self.soc_code_map_file:
            # xx-xxxx for xx-xxxx.00 or xx-xxxx.99
            return self.soc_code_map_file[code[:7]]

        return name

    def build_dict_from_file(self):
        '''
        build occupation_dict and soc_code_map_file
        data from https://www.onetcenter.org/taxonomy/2010/list.html
        key: SOC code : xx-xxxx(.xx)
        value: SOC title

        @type: nothing
        @rtype: nothing
        '''
        with open('./src/2010_Occupations.csv') as file:
            next(file)
            for line in file:
                items = re.split(r',(?=([^\"]*\"[^\"]*\")*[^\"]*$)', line)
                soc_code = tools.clean_soc_code(items[0])
                soc_occupation = tools.clean_soc_name(items[2])
                self.occupation_dict.add(soc_occupation)
                self.soc_code_map_file[soc_code] = soc_occupation
        with open('./src/SOC_Xwalk.csv') as file:
            for line in file:
                cols = re.split(r',(?=([^\"]*\"[^\"]*\")*[^\"]*$)', line)
                soc_occupation = tools.clean_soc_name(cols[6])
                oes_code = tools.clean_soc_code(cols[0])
                if oes_code not in self.soc_code_map_file:
                    self.soc_code_map_file[oes_code] = soc_occupation
                soc_2000_code = tools.clean_soc_code(cols[8])
                if soc_2000_code not in self.soc_code_map_file:
                    self.soc_code_map_file[soc_2000_code] = soc_occupation
                soc_2010_code = tools.clean_soc_code(cols[4])
                if soc_2010_code not in self.soc_code_map_file:
                    self.soc_code_map_file[soc_2010_code] = soc_occupation
        # add special cases mannually
        self.soc_code_map_file['15-1022'] = 'COMPUTER PROGRAMMERS, NON R&D'
        self.soc_code_map_file['15-1023'] = 'COMPUTER PROGRAMMERS, R&D'
        self.soc_code_map_file['15-1034'] = 'SOFTWARE DEVELOPERS, APPLICATIONS, NON R&D'
        self.soc_code_map_file['15-1035'] = 'SOFTWARE DEVELOPERS, APPLICATIONS, R&D'
        self.soc_code_map_file['15-1036'] = 'SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE, NON R&D'
        self.soc_code_map_file['15-1037'] = 'SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE, R&D'
        self.soc_code_map_file['15-1052'] = 'COMPUTER SYSTEMS ANALYSTS, NON R&D'
        self.soc_code_map_file['15-1053'] = 'COMPUTER SYSTEMS ANALYSTS, R&D'
        self.soc_code_map_file['15-1054'] = 'COMPUTER NETWORK ARCHITECTS, NON R&D'
        self.soc_code_map_file['15-1055'] = 'COMPUTER NETWORK ARCHITECTS, R&D'
        self.soc_code_map_file['17-2052'] = 'CIVIL ENGINEERS, NON R&D'
        self.soc_code_map_file['17-2053'] = 'CIVIL ENGINEERS, R&D'
        self.soc_code_map_file['17-2062'] = 'COMPUTER HARDWARE ENGINEERS, NON R&D'
        self.soc_code_map_file['17-2063'] = 'COMPUTER HARDWARE ENGINEERS, R&D'
        self.soc_code_map_file['17-2073'] = 'ELECTRICAL ENGINEERS, NON R&D'
        self.soc_code_map_file['17-2074'] = 'ELECTRICAL ENGINEERS, R&D'
        self.soc_code_map_file['17-2075'] = 'ELECTRONICS ENGINEERS, EXCEPT COMPUTER, NON R&D'
        self.soc_code_map_file['17-2076'] = 'ELECTRONICS ENGINEERS, EXCEPT COMPUTER, R&D'
        self.soc_code_map_file['17-2143'] = 'MECHANICAL ENGINEERS, NON R&D'
        self.soc_code_map_file['17-2144'] = 'MECHANICAL ENGINEERS, R&D'

        self.occupation_dict.add('COMPUTER PROGRAMMERS, NON R&D')
        self.occupation_dict.add('COMPUTER PROGRAMMERS, R&D')
        self.occupation_dict.add('SOFTWARE DEVELOPERS, APPLICATIONS, NON R&D')
        self.occupation_dict.add('SOFTWARE DEVELOPERS, APPLICATIONS, R&D')
        self.occupation_dict.add('SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE, NON R&D')
        self.occupation_dict.add('SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE, R&D')
        self.occupation_dict.add('COMPUTER SYSTEMS ANALYSTS, NON R&D')
        self.occupation_dict.add('COMPUTER SYSTEMS ANALYSTS, R&D')
        self.occupation_dict.add('COMPUTER NETWORK ARCHITECTS, NON R&D')
        self.occupation_dict.add('COMPUTER NETWORK ARCHITECTS, R&D')
        self.occupation_dict.add('CIVIL ENGINEERS, NON R&D')
        self.occupation_dict.add('CIVIL ENGINEERS, R&D')
        self.occupation_dict.add('COMPUTER HARDWARE ENGINEERS, NON R&D')
        self.occupation_dict.add('COMPUTER HARDWARE ENGINEERS, R&D')
        self.occupation_dict.add('ELECTRICAL ENGINEERS, NON R&D')
        self.occupation_dict.add('ELECTRICAL ENGINEERS, R&D')
        self.occupation_dict.add('ELECTRONICS ENGINEERS, EXCEPT COMPUTER, NON R&D')
        self.occupation_dict.add('ELECTRONICS ENGINEERS, EXCEPT COMPUTER, R&D')
        self.occupation_dict.add('MECHANICAL ENGINEERS, NON R&D')
        self.occupation_dict.add('MECHANICAL ENGINEERS, R&D')

