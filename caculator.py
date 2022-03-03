from cgitb import reset


a = [0.03, 0.08, 0.04, 0.03, 0.04, 0.15]


result = 0.0

n = 3

for i in a:
    result = int((1 - (1 - result) * (1 - i)) * 10 ** n) / 10 ** n
    print(result)
