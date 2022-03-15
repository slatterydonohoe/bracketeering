import random


def pickgame(team_1, team_2):
    random.seed()

    seed_total = team_1[1] + team_2[1]
    #print("seed total:" + str(seed_total))
    rnd = random.randint(1, seed_total)
    #print("Rnd: " + str(rnd))

    return team_2 if rnd <= team_1[1] else team_1