# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""
math_operands = ["+","-","/","*","mod"]

def evaluate(ast, env):
    if is_list(ast):
        first = ast[0]
    else:
        first = ast
    if is_closure(first):
        arguments = ast[1:]
        return evaluate(first.body, first.env.extend(evaluate_function_arguments(first, arguments, env)))
    elif is_symbol(first):
        if first == "atom":
            return is_atom(evaluate(ast[1],env))
        elif first == "define":
            if not len(ast[1:]) == 2:
                raise LispError("Wrong number of arguments")
            variable_name = ast[1]
            if not is_symbol(variable_name):
                raise LispError("non-symbol")
            variable_value = evaluate(ast[2], env)
            env.set(variable_name, variable_value)
        elif first == "if":
            evalPredicate = evaluate(ast[1],env)
            if not (is_boolean(evalPredicate)):
                raise LispError('predicate must return boolean value')
            if evalPredicate:
                return evaluate(ast[2], env)
            else:
                return evaluate(ast[3], env)
        elif first == "lambda":
            if not len(ast[1:]) == 2:
                raise LispError("number of arguments")
            params = ast[1]
            body = ast[-1]
            if not (is_list(params)):
                raise LispError('arguments of lambda must be a list')
            return Closure(env, params, body)
        elif first == "quote":
            return ast[1];
        elif first == "eq":
            eval1 = evaluate(ast[1],env)
            eval2 = evaluate(ast[2],env)
            if not (is_atom(eval1) and is_atom(eval2)):  
                return False
            return eval1 == eval2
        elif first in math_operands:
            eval1 = evaluate(ast[1],env)
            eval2 = evaluate(ast[2],env)
            if not (is_integer(eval1) and is_integer(eval2)):  
                raise LispError('math operands must be an integer values')
            return evaluate_math_operation(first, eval1,eval2)
        elif first == "<":
            return evaluate(ast[1], env) < evaluate(ast[2], env)
        elif first == ">":
            return evaluate(ast[1], env) > evaluate(ast[2], env)
        else:
            variable_value = env.lookup(first)
            if is_closure(variable_value):
                return evaluate([variable_value]+ast[1:] , env) 
            return variable_value
    else:
        return first
def evaluate_function_arguments(closure, params_values, env):
    return dict((closure.params[idx], evaluate(param_value, env)) for idx, param_value in enumerate(params_values)) 
def evaluate_math_operation(symbol, eval1, eval2):
    if symbol == "+":
        return eval1 + eval2
    elif symbol == "-":
        return eval1 - eval2
    elif symbol == "/":
        return eval1 / eval2
    elif symbol == "*":
        return eval1 * eval2
    elif symbol == "mod":
        return eval1 % eval2
    else:
        return eval1