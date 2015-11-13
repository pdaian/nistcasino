Motivation, Background, and Whitepaper
--------------------------------

Further discussion of the NIST casino beyond what is in this document is provided in `static/report.pdf`,
and is available at http://45.63.64.229/static/report.pdf for download.  This includes discussions
of the NIST Casino's security guarantees, as well as a comparison to previous work in trusted 
cryptographic games of chance.


Sample Installation
-------------------

A sample deployment of the NIST casino can be accessed at http://45.63.64.229/

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
