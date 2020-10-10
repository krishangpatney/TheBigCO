import os


# x * y is the greatest possible
def greatestProduct(N):
    x = N[0]
    y = N[1]
    if (x > y):
        x, y = y, x
    return (x, y)


# x * y is the lowest possible
def lowestProduct(N):
    if (0 in N):
        return (N[-1], 0)
    # if there's a negative number
    if (N[-1] < 0):
        # get the largest negative
        lN = [x for x in N if x <= 0]
        x = N[0]
        # get smallest positive
        sP = [x for x in N if x >= 0]
        y = N[-1]
    # otherwise, two smallest positives
    else:
        x = N[-1]
        y = N[-2]
    # re-arrange
    if (x > y):
        x, y = y, x
    return (x, y)


# x / y is the greatest possible
def greatestQuo(N):
    if (len(N) <= 2):
        return (N[0], N[1])
    N = [x for x in N if x >= 1]
    N.sort(reverse=True)
    x = N[0]
    y = N[-1]
    return (x, y)


# x / y is the lowest possible
def lowestQuo(N):
    if (len(N) <= 2):
        return (N[1], N[0])
    if (0 in N):
        return (N[-1], 0)
    # if there's a negative number
    if (N[-1] < 0):
        # get the largest negative
        lN = [x for x in N if x <= 0]
        largestNeg = lN[0]
        smallestNeg = lN[-1]
        # get smallest positive
        sP = [x for x in N if x >= 0]
        largestPos = sP[0]
        smallestPos = sP[-1]
        # find the smallest combination
        newN = [smallestNeg, largestNeg, smallestPos, largestPos]
        current = 0.0
        for i in newN:
            for j in newN:
                if (float(i/j) < current):
                    current = float(i/j)
                    x = i
                    y = j
                else:
                    continue
    # otherwise, largest positive, with smallest positive
    else:
        x = N[-1]
        y = N[0]
    return (x, y)


if __name__ == '__main__':
    N = []
    ftpr = open(os.environ['OUTPUT_PATH'], 'w')
    for i in range(2):
        if (i == 1):
            N = input().split(" ")
            N = list(map(int, N))
            #N = [-1,-2]
            N.sort(reverse=True)
            x = greatestProduct(N)[0]
            y = greatestProduct(N)[1]
            ftpr.write(str(x) + " " + str(y) + '\n')
            x = lowestProduct(N)[0]
            y = lowestProduct(N)[1]
            ftpr.write(str(x) + " " + str(y) + '\n')
            x = greatestQuo(N)[0]
            y = greatestQuo(N)[1]
            ftpr.write(str(x) + " " + str(y) + '\n')
            x = lowestQuo(N)[0]
            y = lowestQuo(N)[1]
            ftpr.write(str(x) + " " + str(y) + '\n')
            break
        input()
    ftpr.close()
