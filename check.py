import time
from casinochain import *
from config import *
from lottogame import *
from cointossgame import *

c = CasinoChain()
game = CoinTossGame()
if (int(raw_input("Lotto [1] or CoinToss [2]? ").strip()) == 1):
    game = LottoGame()
c.load_and_verify_plaintext_chain(open(raw_input('Enter a file name with a chain saved in it to verify chain and winners offline: ')).read().strip(), game)

print "[+] No errors means success!"
