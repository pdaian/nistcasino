import json, random

class CoinTossGame:
    def is_valid_ticket(self, ticket):
        try:
            num_tosses = int(ticket)
            return (num_tosses > 0 and num_tosses < 51)
        except:
            return False

    def get_game_result(self, chain, randint):
        r = random
        r.seed(randint)
        result = ''
        result += 'Using trusted rand int ' + str(randint) + ' as RNG seed- Requested tosses:\n' 
        for block in chain[1:]:
            block = json.loads(block)
            for transaction in block['transactions']:
                ticket = transaction['ticket']
                if not self.is_valid_ticket(transaction['ticket']):
                    return 'Error: invalid transaction ' + str(transaction)
                ticket_value = int(ticket)
                result += transaction['id'] + ' coin tosses (1=heads): '
                for i in range(0, ticket_value):
                    result += str(r.randint(0, 1))
                result += '\n'
        return result

    def get_id(self):
        return 'CoinToss'
