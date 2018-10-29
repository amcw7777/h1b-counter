'''
Implementation of useful function in H1B data analysis.

clean_soc_code: transfer soc_code to a format as 'xx-xxxx.xx'
clean_soc_name: fix some typos and strip space and quota
split: split a string with input saperator, keep content in quota

Usage:
    import h1b_tools as tools
    tools.clean_soc_code('123456') -> return '12-3456.00'
    tools.split('xx;"xxx;xx";x') -> return ['xx', '"xxx;xx"', 'x']

Author and Mainainer:
    Liang He (liangheNOSPAM@gmail.com)
'''

def clean_soc_code(code):
    '''
    clean soc_code to a format as xx-xxxx(.xx)
    @type code: string
    @rtype: string
    '''
    if not code:
        return ''
    new_code = ''
    for num in code:
        if not num.isdigit():
            continue
        new_code += num
    new_code = new_code[:2] + '-' + new_code[2:] # format xx-xxxx
    if len(new_code) > 7:
        new_code = new_code[:7]+'.'+new_code[7:] # format xx-xxxx.xx
    elif len(new_code) == 7:
        new_code += '.00'
    if new_code.endswith('.99'):
        new_code = new_code[:7]+'.00'

    return new_code

def clean_soc_name(name):
    '''
    clean soc_name
    modify topos, strip '"' and '*', all letter capital
    @type name: string
    @rtype: string
    '''
    if not name:
        return ''
    name = name.strip('"')
    name = name.upper()
    if ' & ' in name:
        name = name.replace(' & ', ' AND ')
    if '*' in name:
        '''
        Name ends with '*' means this soc is differently defined in SOC2010 and SOC2000
        '''
        name = name.strip('*')
    return name

def split(s, sep):
    '''
    split a string with separater
    consider the case with quota 'xx;"xxx;xx";x' -> ['xx', '"xxx;xx"', 'x']
    @type s: string
    @tpye sep: char (',', ';', etc...)
    @rtype: list of string
    '''
    n = len(s)
    i = 0
    res = []
    while i < n:
        temp = ''
        quota = False
        while i < n and (s[i] != sep or quota):
            temp += s[i]
            if s[i] == '"':
                quota = not quota
            i += 1
        res.append(temp)
        i += 1
    return res


