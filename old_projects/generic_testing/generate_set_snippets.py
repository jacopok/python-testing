qm_commands0 = {'geq', 'leq', 'forall', 'exists', 'dag', 'cdot', 'iff', 'hbar'}
qm_commands1 = {'ket', 'bra', 'dyad', 'expval'}
qm_commands2 = {'braket', 'ketbra', 'pdv', 'dv', 'fdv'}

new0 = {'otimes', 'divisionsymbol', 'sim', 'leftrightarrow', 'equiv', 'log'}
new1 = {'abs', 'sqrt', 'P', 'sin', 'cos', 'tan'}

def no_arguments(commands):
    for c in commands:
        print(f'\'Command {c}\':')
        print(f'  \'prefix\': \'{c}\'')
        print(f'  \'body\': \'\\\\\\\\{c}\' ')
        print()

def one_argument(commands):
    for c in commands:
        print(f'\'Command {c}\':')
        print(f'  \'prefix\': \'{c}\'')
        print(f'  \'body\': \'\\\\\\\\{c}{{$1}} $2\'')
        print()

def two_argument(commands):
    for c in commands:
        print(f'\'Command {c}\':')
        print(f'  \'prefix\': \'{c}\'')
        print(f'  \'body\': \'\\\\\\\\{c}{{$1}}{{$2}} $3\'')
        print()

#no_arguments(qm_commands0)
# one_argument(qm_commands1)
# two_argument(qm_commands2)

no_arguments(new0)
one_argument(new1)

"""
  'Modulus':
    'prefix': 'mod'
    'body': '\\\\mod'
"""
