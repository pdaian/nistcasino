import json

class LottoGame:
    def is_valid_ticket(self, ticket):
        try:
            dollar_value = int(ticket)
            return (dollar_value > 0)
        except:
            return False

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

    def get_id(self):
        return 'Lotto'
