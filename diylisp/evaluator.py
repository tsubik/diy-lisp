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
        first_exp = ast[0]
        if first_exp == "atom":     return is_atom(evaluate(ast[1],env))
        elif first_exp == "define": return eval_define(ast[1:], env)
        elif first_exp == "if":     return eval_if_statement(ast[1:], env)
        elif first_exp == "lambda": return eval_lambda(ast[1:], env)
        elif first_exp == "quote":  return ast[1];
        elif first_exp == "eq":     return eval_equation(ast[1:], env)
        elif first_exp == "cons":   return eval_list_cons(ast[1:], env)
        elif first_exp == "head":   return eval_list_head(ast[1:], env)    
        elif first_exp == "tail":   return eval_list_tail(ast[1:], env)  
        elif first_exp == "empty":  return eval_list_empty(ast[1:], env)
        elif first_exp in math_operands:    return eval_math_operation(first_exp, ast[1:], env)
        elif first_exp == "<":  return evaluate(ast[1], env) < evaluate(ast[2], env)
        elif first_exp == ">":  return evaluate(ast[1], env) > evaluate(ast[2], env)
        elif is_list(first_exp) or is_symbol(first_exp): 
            eval_first = evaluate(first_exp, env)
            return evaluate([eval_first]+ast[1:], env)
        elif is_closure(first_exp):
            arguments = ast[1:]
            return evaluate(first_exp.body, first_exp.env.extend(evaluate_function_arguments(first_exp, arguments, env)))
        else:
            raise LispError('not a function')

    elif is_symbol(ast): return env.lookup(ast)
    elif is_atom(ast): return ast    

def eval_list_cons(args, env):
    elem = evaluate(args[0], env)
    _list = evaluate(args[1], env)
    return [elem] + _list

def eval_list_head(args, env):
    _list = evaluate(args[0], env)
    if len(_list)==0:
        raise LispError('empty list')
    return _list[0]

def eval_list_tail(args, env):
    _list = evaluate(args[0], env)
    if len(_list)==0:
        raise LispError('empty list')
    return _list[1:]

def eval_list_empty(args, env):
    _list = evaluate(args[0], env)
    return len(_list)==0

def eval_define(args, env):
    if not len(args) == 2:
        raise LispError("Wrong number of arguments")
    variable_name = args[0]
    if not is_symbol(variable_name):
        raise LispError("non-symbol")
    variable_value = evaluate(args[1], env)
    env.set(variable_name, variable_value)
def eval_if_statement(args, env):
    evalPredicate = evaluate(args[0],env)
    if not (is_boolean(evalPredicate)):
        raise LispError('predicate must return boolean value')
    if evalPredicate:
        return evaluate(args[1], env)
    else:
        return evaluate(args[2], env)
def eval_equation(args, env):
    eval1 = evaluate(args[0],env)
    eval2 = evaluate(args[1],env)
    if not (is_atom(eval1) and is_atom(eval2)):  
        return False
    return eval1 == eval2
def eval_lambda(args, env):
    if not len(args) == 2:
        raise LispError("number of arguments")
    params = args[0]
    body = args[-1]
    if not (is_list(params)):
        raise LispError('arguments of lambda must be a list')
    return Closure(env, params, body)
def eval_math_operation(symbol, args, env):
    eval1 = evaluate(args[0],env)
    eval2 = evaluate(args[1],env)
    if not (is_integer(eval1) and is_integer(eval2)):  
        raise LispError('math operands must be an integer values')
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
def evaluate_function_arguments(closure, params_values, env):
    params_count = len(params_values) 
    closure_params_count = len(closure.params) 
    if params_count != closure_params_count:
        raise LispError("wrong number of arguments, expected {0} got {1}".format(closure_params_count, params_count))
    return dict((closure.params[idx], evaluate(param_value, env)) for idx, param_value in enumerate(params_values)) 