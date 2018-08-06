from itertools import combinations, permutations, product

def reverse_polish(expression):
    ops = {
        "+": (lambda a, b: a + b),
        "-": (lambda a, b: a - b),
        "*": (lambda a, b: a * b),
        "/": (lambda a, b: a / b)
    }
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in ops:
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = ops[token](arg1, arg2)
            stack.append(result)
        else:
            stack.append(int(token))

    return stack.pop()


def countdown_solver(goal, nr_list):
    # Works but re-uses values (Cheats)
    nr_combinations = combinations(nr_list, 2)
    permutat = []
    for i in nr_combinations:
        permutat.append("+".join(i))
        permutat.append("-".join(i))
        permutat.append("*".join(i))
        permutat.append("/".join(i))
    perm_comb = combinations(permutat, 3)
    overall = []
    for trio in perm_comb:
        overall.append("+".join(trio))
        overall.append("-".join(trio))
        overall.append("*".join(trio))
        overall.append("/".join(trio))
    for i in overall:
        if eval(i) == goal:
            print("{} = {}".format(i, eval(i)))


def countdown_solver_ii(goal, nr_list, length):
    # Doesn't work but not sure quite why
    operators = ['+', '-', '*', '/']
    nr_combs = permutations(nr_list, length)
    op_combs = product(operators, repeat=length-1)
    for nr, op in zip(nr_combs, op_combs):
        result = [None] * (len(nr) + len(op))
        result[::2] = nr
        result[1::2] = op
        stri = ''.join(result)
        answer = eval(stri)
        #if int(answer) == int(goal):
        print('{} = {}'.format(stri, answer))

def length_compensate(goal, nr_list):
    i = 6
    while i > 1:
        countdown_solver_ii(goal, nr_list, i)
        i -= 1


if __name__ == '__main__':
    countdown_solver(609, ['50', '75', '4', '4', '1', '3'])