summ = []


def nums():
    global summ
    n = int(input())
    if n != 0:
        summ.append(n)
        nums()
    else:
        print(sum(summ) / len(summ))


nums()
