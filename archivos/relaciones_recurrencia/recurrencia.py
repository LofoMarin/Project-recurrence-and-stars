import sympy as sp
from sympy import *


def solve_recurrence(relation, initial_conditions):
    '''
    Main routine to solve almost any recurrence relation

    This is a wrapper to be used in .commands.py
    '''

    initial_conditions = initial_conditions.split(",")

    f_conditions = {}

    for condition in initial_conditions:

        f = sp.parse_expr(condition.split("=")[0])
        f_value = condition.split("=")[1]

        f_conditions[f] = int(f_value)

    # Convert str to symbolic expressions
    parsed_relation = sp.parse_expr(relation)

    terms = (
        parsed_relation.args
        if isinstance(parsed_relation, sp.Add)
        else [parsed_relation]
    )
    homogen_terms = [term for term in terms if 'f(n -' in str(term)]
    if part_terms := [term for term in terms if 'f(n -' not in str(term)]:
        # --- Solve
        fn_part = solve_part_relation(terms, f_conditions)
        return f'f(n) = {sp.latex(fn_part)}'
    else:
        # --- Solve
        fn_homogen = solve_homogen_relation(homogen_terms, f_conditions)
        return f'f(n) = {sp.latex(fn_homogen)}'


def solve_homogen_relation(homogen_terms, f_conditions):
    '''
    Subroutine to solve homogeneous RR
    '''

    # Define
    f = Function('f')
    n = symbols('n')

    # Function to use
    function = f(n)

    # Add terms
    for term in homogen_terms:
        function -= term

    return rsolve(function, f(n), f_conditions)


def solve_part_relation(terms, f_conditions):
    '''
    Subroutine to solve particular RR
    '''

    # Define
    f = Function('f')
    n = symbols('n')

    # Function to use
    function = f(n)

    # Add terms
    for term in terms:
        function -= term

    return rsolve(function, f(n), f_conditions)