import copy
import itertools


class Particle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.hitCounter = 0
        self.surviveProb = -1

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.vx) + " " + str(self.vy)

    def stepBack(self):
        self.x -= self.vx
        self.y -= self.vy

    def stepForward(self):

        tmpX = self.x + self.vx
        tmpY = self.y + self.vy

        if tmpX > S or tmpX < -S:
            self.hitCounter += 1
            outOfBound = abs(tmpX) - S
            velocityPercentage = abs(outOfBound/self.vx)

            self.x += (1-velocityPercentage) * self.vx
            self.vx = - self.vx
            self.x += velocityPercentage * self.vx
        else:
            self.x = tmpX

        if tmpY > S or tmpY < -S:
            self.hitCounter += 1
            outOfBound = abs(tmpY) - S
            velocityPercentage = abs(outOfBound / self.vy)

            self.y += (1-velocityPercentage) * self.vy
            self.vy = - self.vy
            self.y += velocityPercentage * self.vy
        else:
            self.y = tmpY


    def manhattanDistance(self):
        return abs(self.x) + abs(self.y)

    def calcSurviveProb(self, p):
        self.surviveProb = p ** self.hitCounter


if __name__ == "__main__":

    N, S, T, P = input().split(" ")
    N = int(N)
    S = int(S)
    T = int(T)
    P = float(P)
    particleList = []

    for i in range(N):
        xtmp, ytmp, vxtmp, vytmp = (float(k) for k in input().split(" "))
        particleList.append( Particle(xtmp, ytmp, vxtmp, vytmp) )

    tmp = copy.deepcopy(particleList)

    minDistSum = float('inf')
    currDistSum = 0
    counter = 0

    for particle in particleList:
        currDistSum += particle.manhattanDistance()

    while True:
        if currDistSum > minDistSum:
            break

        minDistSum = currDistSum
        currDistSum = 0
        counter += 1

        for particle in particleList:
            particle.stepBack()
            currDistSum += particle.manhattanDistance()

#################################

    particleList = tmp
    hitSumm = 0

    for i in range(T):
        for particle in particleList:
            particle.stepForward()

    for particle in particleList:
        particle.calcSurviveProb(P)
        hitSumm += particle.hitCounter

##################################

    expectedValue = 0
    for particle in particleList:
        expectedValue += particle.surviveProb

    print(counter - 1, hitSumm, expectedValue)