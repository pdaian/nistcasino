import json, uuid, beacon, time, threading, hashlib
from config import *

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode

class CasinoChain:
    key = ""
    pending_transactions = []
    final_entropy_block = None
    blocks = []
    active = True
    game = None
    initialized = False
    ending_timestamp = ""
    beacon = beacon.Beacon()
    checker_thread = None
    latest_beacon_val = None
    done = False

    def print_chain(self):
        for block in self.blocks:
            print block

    def get_time_remaining(self):
        tr = int(self.ending_timestamp) - int(json.loads(self.blocks[-1])['beacon'][0])
        if (tr < 0):
            return 0
        return tr

    def parse_chain(self, chain_string):
        for block in chain_string.splitlines():
            self.blocks.append(block)

    def is_active(self):
        return len(self.blocks) > 0 and self.active

    def is_done(self):
        return self.done

    def add_to_chain(self, transaction):
        if not self.active:
            return "Error: Sorry, this game is not taking any new entries."
        if self.is_valid_transaction(transaction):
            self.pending_transactions.append(transaction)
            transaction['id'] = str(uuid.uuid4())
            return "Successfully queued your transaction for inclusion.  Please look for TX '" + transaction['id'] + "' in the chain."
        return "Error:  Ticket request invalid or signature incorrect."

    def initialize_first_block(self, game):
        if (self.initialized):
            raise Exception("initialized called twice")
        self.game = game
        game_id = str(uuid.uuid4())
        self.latest_beacon_val = self.beacon.last_record()
        self.ending_timestamp = int(self.latest_beacon_val['timeStamp']) + GAME_LENGTH_SECONDS
        block = {'game_params': [self.get_game_id(), self.ending_timestamp, game_id], 'dealer_public_key': RSA_PUBKEY}
        block['beacon'] = [self.latest_beacon_val['timeStamp'], self.latest_beacon_val['outputValue']]
        block['signed_message'] = [self.get_game_id(), str(self.ending_timestamp), game_id, self.latest_beacon_val['outputValue'], self.latest_beacon_val['timeStamp']]
        block['signature']  = self.sign('|'.join(block['signed_message']), RSA_PRIVKEY)
        self.blocks = [json.dumps(block)]
        self.checker_thread = threading.Thread(target = self.update_chain, args=(), kwargs={})
        self.checker_thread.start()
        self.initialized = True

    def is_valid_transaction(self, transaction):
        if not self.verify(transaction['ticket'], transaction['signature'], transaction['key']):
            return False
        return self.game.is_valid_ticket(transaction['ticket'])

    def get_result(self):
        #if not self.done:
        #    return 'Error! Game still in progress'
        self.verify_integrity(self.blocks)
        return self.game.get_game_result(self.blocks, int(json.loads(self.blocks[-1])['beacon'][1], 16))

    def get_game_id(self):
        return self.game.get_id()

    def sign(self, message, key):
        rsakey = RSA.importKey(key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(message)
        sign = signer.sign(digest)
        return b64encode(sign)         

    def verify(self, message, signature, pub_key):
        rsakey = RSA.importKey(pub_key)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(message)
        if signer.verify(digest, b64decode(signature)):
            return True
        return False 

    def update_chain(self):
        while True:
            latest_record = self.beacon.last_record()
            latest_time = int(latest_record['timeStamp'])
            if (latest_time - int(self.latest_beacon_val['timeStamp']) != 0):
                self.latest_beacon_val = latest_record
                latest_time = int(latest_record['timeStamp'])
                if (self.ending_timestamp - latest_time <= 0):
                    self.latest_beacon_val = self.beacon.current_record(str(self.ending_timestamp))
                    self.done = True
                block = {'transactions': self.pending_transactions}
                self.pending_transactions = []
                block['beacon'] = [self.latest_beacon_val['timeStamp'], self.latest_beacon_val['outputValue']]
                block['signed_message'] = [json.dumps(block['transactions']), hashlib.sha256(self.blocks[-1]).hexdigest(), self.latest_beacon_val['outputValue'], self.latest_beacon_val['timeStamp']]
                block['signature']  = self.sign('|'.join(block['signed_message']), RSA_PRIVKEY)
                self.blocks.append(json.dumps(block))
                if self.done:
                    return
            if (self.ending_timestamp - latest_time <= BOOKKEEPING_PERIOD):
                self.active = False
            time.sleep(5)

    def load_and_verify_plaintext_chain(self, chain, game):
        self.game = game
        pyChain = chain.split('\n\n')
        pyChain = [block.strip() for block in pyChain]
        print pyChain
        print "[+] Chain successfully imported.  Verifying integrity."
        return self.verify_integrity(pyChain)

    def verify_integrity(self, blocks):
        if len(blocks) == 0:
            return False
        first_block = json.loads(blocks[0])
        game_params = first_block['game_params']
        dealer_pk = first_block['dealer_public_key']
        game_type = game_params[0]
        game_end_time = game_params[1]
        game_id = game_params[2]
        beacon_vals = first_block['beacon']

        # Check that first block is properly signed
        signed_message = first_block['signed_message']
        if signed_message[0] != game_type or int(signed_message[1]) != int(game_end_time) or signed_message[2] != game_id:
            print "Error in signature parameters of first block.  Integrity check failed."
            return False
        if signed_message[3] != beacon_vals[1] or signed_message[4] != beacon_vals[0]:
            print "Error in signature parameters of first block.  Beacon signature integrity check failed."
            return False
        if not self.verify('|'.join(signed_message), first_block['signature'], dealer_pk):
            print "Error in signature parameters of first block.  Signature verification failed."
            return False

        for block_num in range(0, len(blocks)):
            block = json.loads(blocks[block_num])
            
            # Check that block beacon values are consistent with NIST
            block_beacon_vals = block['beacon']
            desired_record = self.beacon.current_record(timestamp = block_beacon_vals[0])
            if (desired_record['outputValue'] != block_beacon_vals[1]):
                print "Error in NIST beacon check.  Possible NIST value forgery."
                return False    

            if block_num != 0: # For all but first block
                # Check that block is properly signed with valid house signature values
                signed_message = block['signed_message']
                if (json.loads(signed_message[0]) != block['transactions']): 
                    #or (signed_message[2] != block_beacon_vals[1]) or (signed_message[3] != block_beacon_vals[0]):
                    print "Error.  Block validation failed to validate plaintext signed message contents."
                    return False
                if (signed_message[1] != hashlib.sha256(blocks[block_num-1]).hexdigest()):
                    print "Error.  Block validation failed to validate previous block hash.  Possible block insertion attack at block " + str(i)
                    return False

                if not self.verify('|'.join(signed_message), block['signature'], dealer_pk):
                    print "Error.  Block validation failed to validate block signature.  Possible block insertion attack at block " + str(i)
                    return False
                   
               # Check that block occured after last block and has correct hash for last block
                if (int(block['beacon'][0]) <= int(json.loads(blocks[block_num-1])['beacon'][0])):
                    print "Error in block times.  Block " + str(block_num) + " is predated."

                # Check that each transaction is valid (signed with a valid game ticket)
                for transaction in block['transactions']:
                    if not self.is_valid_transaction(transaction):
                        print "Error in transaction validation.  Transaction " + transaction['id'] + " is invalid."
                        return False    
        return True
