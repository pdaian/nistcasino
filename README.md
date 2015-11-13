Motivation, Background, and Whitepaper
--------------------------------

Further discussion of the NIST casino beyond what is in this document is provided in `static/report.pdf`,
and is available at http://45.63.64.229:5000/static/report.pdf for download.  This includes discussions
of the NIST Casino's security guarantees, as well as a comparison to previous work in trusted 
cryptographic games of chance.


Sample Installation
-------------------

A sample deployment of the NIST casino can be accessed at http://45.63.64.229:5000/

Note that this deployment operates over HTTPS, and should not be trusted with games whose outcome affects
real funds.


Installation
-------------

To install, simply:

- Install Python, Python-pip
- Install PyCrypto dependencies (on Ubuntu/Debian, sudo apt-get install libgmp-dev build-essential python-dev)
- sudo pip install -r requirements.txt


Running
-------

To run the NIST Casino after installation, simply change the values in config.py and run
`python web_interface.py` from the main folder.


Playing
-------

To play a NIST casino game, a player must first generate a ticket.  
A ticket request, sent to the house, includes only the public key of a player-stored RSA 
key.  The ticket request can be generated either server or client-side, for a balance 
of trustless operation and ease of use.

The public key is provided to the NIST casino as a ticket request, after which it is encoded into
a ticket.  The ticket includes an RSA public key and all of the parameters required to process
the user's action in a given game (for example, Blackjack-like games can include a 'hit or stay'
parameter determining user action).  The ticket is then saved by the user as "proof of purchase",
along with their private key (required to claim winnings if they have the winning ticket).  A 
ticket is also signed by the house once it is accepted, so that if the house attempts to later
revoke the ticket, valid proof of purchase can be proven by the user.

Each game has a "casino chain", which consists of one block every sixty seconds containing all the
tickets sold during that time period.  The initial casino chain block also contains the dealer's
RSA key information and the game parameters, used to compute the final outcome when the game is finished
and to sign users' tickets as they are distributed.

Each block is timestamped, signed by the dealer, carries a hash reference to the previous block (for 
unmodifiability), and contains the NIST beacon value released after block creation (to prevent precomputation
of blocks by the house).  For the dealer to modify any user's ticket in the chain, it would also have
to modify subsequent blocks, an obvious attack that is easily detectable.

The game ends after the time period defined in the initial block has elapsed.  Once the game ends, the NIST 
Casino page will display a winner.  Users can also verify the winner locally by running 
`python check.py` and inputting a file containing the full caino chain to check.  This will verify that
each block has the correct NIST beacon value and is correctly signed by both dealers and participants.

An example chain is provided for use with the checking utility in the `example_chain` file.


Determining Winners and Creating New Games
-------------------------------------------

As previously stated, winners can be computed entirely client side.  The rules by which winners are
decided are written as an easily auditable Python program.  This program must implement three functions:

```
    def get_id(self)
    def is_valid_ticket(self, ticket)
    def get_game_result(self, chain, randint)

```

The first function, `get_id`, simply returns the plaintext game name (eg - 'Lotto').

The second function, `is_valid_ticket`, takes a ticket object and returns whether the ticket should
be considered valid.  Only valid tickets are considered in the computation of the final winner.  An 
example of the valid ticket rules for the Lotto game are as follows:

```
    def is_valid_ticket(self, ticket):
        try:
            dollar_value = int(ticket)
            return (dollar_value > 0)
        except:
            return False
```

where a valid ticket has a positive integer dollar amount associated with it.

The last function, get_game_result, takes a Casino chain (downloadable from the house) and a random
integer value.  This value is obtained from the NIST beacon API, using the block generated at the
predetermined time and encoded in the first block of the casino chain.  It is intended to be easily
auditable and simple.  Here it is for a basic lottery:

```
    def get_game_result(self, chain, randint):
        result = ''
        total_tickets = 0
        # Calculate total number of tickets, ignoring first block
        for block in chain[1:]:
            block = json.loads(block)
            for transaction in block['transactions']:
                ticket = transaction['ticket']
                if not self.is_valid_ticket(transaction['ticket']):
                    return 'Error: invalid transaction ' + str(transaction)
                total_tickets += int(ticket)
        if (total_tickets == 0):
            return 'No winner! No tickets sold :('
        # Use entropy to calculate winning ticket
        result += 'Total tickets: ' + str(total_tickets) + '\n'
        winning_ticket = randint % total_tickets
        result += 'Winning ticket: ' + str(winning_ticket) + '\n'
        current_ticket = 0
        # Find winning ticket in chain and return
        for block in chain[1:]:
            block = json.loads(block)
            for transaction in block['transactions']:
                ticket_value = int(transaction['ticket'])
                if ((current_ticket + ticket_value) > winning_ticket) and (current_ticket <= winning_ticket):
                    result += 'Won on index ' + str(current_ticket) + '\n'
                    result += 'Winning transaction (ID ' + transaction['id'] + '):' + str(transaction)
                    return result
                current_ticket += ticket_value
        return 'Error: No winner found.'
```

As previously mentioned, each ticket has a dollar amount.  The total number of dollars sold (total_tickets) is
first calculated.  Then, the winner is calculated from the entropy modulo the sales.  The winning ticket is 
identified in the chain and printed to the screen.


Other Games
-----------

We also include CoinToss, a game where each user submits a ticket with a number of coin tosses they would like
performed.  The result is a sequence of non-precomputable coin tosses, and can be used for remote coin tosses
where fairness is critical.

Other more advanced games, like Blackjack, Roulette, and traditional casino games, are easily encodable into
the above framework.  For simplicity (both legal and technical), we do not include such games.


Further Avoiding Precomputation
--------------------------------

The last block of any casino chain must be empty (with more empty blocks potentially
required based on configuration).  This is to prevent manipulation of the last block by the house 
after the NIST entropy source is revealed, and to give players the time to download the
unaltered chain for independent output computation before the outcome is determined by
the entropy reveal by NIST.
