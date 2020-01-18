import re
from sympy import sympify
from sympy.parsing.sympy_parser import parse_expr

replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    '^': '**',
}

allowed_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
]

def str2func1D(string):
    ''' evaluates the string and returns a function of x '''
    # find all words and check if all are allowed:
    for word in re.findall('[a-zA-Z_]+', string):
        if word not in allowed_words:
            raise ValueError(
                '"{}" is forbidden to use in math expression'.format(word)
            )

    for old, new in replacements.items():
        string = string.replace(old, new)


    return 0

def string2func1D(string):
    ldict = {}
    string = 'a = lambda x: {}'.format(string)
    print(string)
    exec(string, globals(),ldict)
    a = ldict['a']
    return a