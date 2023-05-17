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

    # Get all the terms of the relation
    if isinstance(parsed_relation, sp.Add):
        terms = parsed_relation.args
    else:
        terms = [parsed_relation]

    # HOMOGENEOUS PART
    # --- Split
    homogen_terms = []
    for term in terms:
        if 'f(n -' in str(term):
            homogen_terms.append(term)

    # PARTICULAR PART
    # --- Split
    part_terms = []
    for term in terms:
        if 'f(n -' not in str(term):
            part_terms.append(term)

    if len(part_terms) == 0:
        # --- Solve
        fn_homogen = solve_homogen_relation(homogen_terms, f_conditions)
        return 'f(n) = ' + sp.latex(fn_homogen)
    else:
        # --- Solve
        fn_part = solve_part_relation(part_terms, f_conditions)
        return 'f(n) = ' + sp.latex(fn_part)


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

    # Solve
    fn_solved = rsolve(function, f(n), f_conditions)

    return fn_solved


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

    # Solve
    fn_solved = rsolve(function, f(n), f_conditions)

    return fn_solved
