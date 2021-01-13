import random
import matplotlib.pyplot as plt
import time

N = 1  # Decks Count
iterations = 1000  # How many random games for each set analyzed

# Number of calculations in for loops :
# len(card_types)*len(card_types)*iterations
# 169 * iterations

UserWins = 0
CasinoWins = 0
card_types = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
colors = 4
casinoAsesCount = 0


def deck_init():
    decks = [0 for x in range(len(card_types)*N*colors)]
    for i in range(N):
        for j in range(colors):
            for k in range(len(card_types)):
                decks[i*len(card_types)*colors + j *
                      len(card_types) + k] = card_types[k]
    return decks


def random_card_set(decks):
    random.shuffle(decks)
    usrCard_1 = decks[0]
    croupierCard = decks[1]
    usrCard_2 = decks[2]
    card_set = [usrCard_1, usrCard_2, croupierCard]
    return card_set


def after_draw(decks, card_set):
    decks.remove(card_set[0])
    decks.remove(card_set[1])
    decks.remove(card_set[2])


def usr_points(card_set):
    points = 0
    for i in range(2):
        if not str(card_set[i]).isnumeric() and card_set[i] != 'A':
            points += 10
        if card_set[i] == 'A':
            points += 11
        if str(card_set[i]).isnumeric():
            points += card_set[i]
    if points == 22:
        points = 12
    return points


def card_points(card):
    global casinoAsesCount
    if not str(card).isnumeric() and card != 'A':
        points = 10
    if card == 'A':
        points = 11
        casinoAsesCount += 1
    if str(card).isnumeric():
        points = card
    return points


def casino_play(casinoPoints):
    global casinoAsesCount
    while True:
        card = decks[0]
        casinoPoints += card_points(card)
        decks.remove(card)
        if casinoPoints > 21 and casinoAsesCount > 0:
            casinoPoints -= 10
            casinoAsesCount -= 1
        if casinoPoints >= 17 or casinoPoints >= userPoints:
            break
    return casinoPoints


def who_wins(usrPoints, casinoPoints):
    global CasinoWins
    global UserWins
    if usrPoints == 21:
        UserWins += 1
    else:
        if casinoPoints > 21:
            UserWins += 1
        else:
            if usrPoints > casinoPoints:
                UserWins += 1
            else:
                CasinoWins += 1


start = time.time()

WinRatio = [[0 for x in range(len(card_types))]
            for y in range(len(card_types))]
BarNames = [[0 for x in range(len(card_types))]
            for y in range(len(card_types))]

fig = plt.figure()
plt.suptitle('Probability of winning graphs')
for card1 in range(len(card_types)):
    for card2 in range(len(card_types)):
        UserWins = 0
        casinoAsesCount = 0
        print("-------------------------- ")
        print('User Cards : ' + str(card_types[card1]) +
              ', ' + str(card_types[card2]))
        print("-------------------------- \n")
        for i in range(iterations):
            decks = deck_init()
            card_set = random_card_set(decks)
            card_set[0] = card_types[card1]
            card_set[1] = card_types[card2]
            after_draw(decks, card_set)
            userPoints = usr_points(card_set)
            casinoPoints = card_points(card_set[2])
            casinoPoints = casino_play(casinoPoints)
            who_wins(userPoints, casinoPoints)
        print(str(UserWins) + '\n')
        WinRatio[card1][card2] = UserWins/iterations*100
        BarNames[card1][card2] = str(card_types[card2])
    plt.subplot(4, 4, card1+1)
    plt.bar(BarNames[card1], WinRatio[card1])
    plt.title('First card : ' + str(card_types[card1]))
    plt.ylim(0, 100)
    plt.ylabel('% of wins')

timeElapsed = abs(start - time.time())
print('\n' + str(iterations) + ' Iterations took ' +
      str(timeElapsed) + ' seconds.')
plt.subplots_adjust(0.05, 0.04, 0.97, 0.92, 0.2, 0.3)
plt.show()
