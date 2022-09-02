# This entrypoint file to be used in development. Start by reading README.md
from RPS_game import play, mrugesh, abbey, quincy, kris, human, random_player, abbey_three
from RPS import player
from unittest import main

# play(player, quincy, 1000)
# play(player, abbey, 1000)
# play(player, kris, 100)
# play(player, mrugesh, 1000)
# play(player, abbey_three, 1000)
# play(abbey_three, abbey, 10000)
# Uncomment line below to play interactively against a bot:
# play(human, abbey, 21, verbose=True)


# Uncomment line below to play against a bot that plays randomly:
# play(human, random_player, 21)

# Uncomment line below to run unit tests automatically
# main(module='test_module', exit=False)

# players = {0:quincy,1:abbey,2:kris,3:mrugesh}
players = [quincy, abbey, kris, mrugesh]
for j in players:
    for k in players:
        print(j.__name__, ' vs. ', k.__name__)
        play(j,k,1000000)
    print()


