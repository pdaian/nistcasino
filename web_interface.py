from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from config import *
from casinochain import *
from lottogame import *
from cointossgame import *
import json

app = Flask(__name__)

# Enable Lotto and Coin Toss games
app.NIST_GAMES_AVAILABLE = {'Lotto': LottoGame, 'CoinToss': CoinTossGame}
app.latest_game_id = 2
app.games = {0: CasinoChain(), 1: CasinoChain()}
app.curr_game_ids = {'Lotto': 0, 'CoinToss': 1}
app.games[0].initialize_first_block(LottoGame())
app.games[1].initialize_first_block(CoinTossGame())

def get_or_current_id(id, game_type):
    if not game_type in app.curr_game_ids:
        return None
    if id is not None:
        id = int(id)
        if id in app.games:
            return id
        return None
    if (app.games[app.curr_game_ids[game_type]].is_active() and not app.games[app.curr_game_ids[game_type]].is_done()):
        return app.curr_game_ids[game_type]
    curr_id = app.latest_game_id
    app.latest_game_id += 1
    app.games[curr_id] = CasinoChain()
    app.games[curr_id].initialize_first_block(app.NIST_GAMES_AVAILABLE[game_type]())
    app.curr_game_ids[game_type] = curr_id
    return curr_id

@app.route('/')
def hello():
    return render_template('hello.html', games_available = app.NIST_GAMES_AVAILABLE)

@app.route('/play/<string:game>/')
@app.route('/play/<string:game>/<string:id>')
def play(game, id = None):
    curr_id = get_or_current_id(id, game)
    if (id is None):
        return redirect(url_for('play', game = game, id = curr_id))
    return render_template('play.html', game_id = curr_id, game = app.games[curr_id])

@app.route('/gen_ticket/<string:game>/<string:id>')
def gen_ticket(game, id):
    id = int(id)
    message = "5"
    new_key = RSA.generate(2048, e=65537)
    public_key = new_key.publickey().exportKey("PEM")
    private_key = new_key.exportKey("PEM")
    return render_template('gen_ticket.html', game_id = id, game = app.games[id], priv_key = private_key, payload = json.dumps({'key': public_key, 'signature': app.games[id].sign(message, private_key), 'ticket': message}))

@app.route('/submit_new_ticket/<game_type>/<id>', methods=['POST'])
def submit(game_type, id = None):
    game = app.games[int(id)]
    message = game.add_to_chain(json.loads(request.form['payload']))
    return render_template('add.html', message = message, game_type = game_type, game_id = id)

@app.route('/view_chain/<game>/')
@app.route('/view_chain/<game>/<id>')
def view_chain(game, id = None):
    curr_id = get_or_current_id(id, game)
    if (id is None):
        return redirect(url_for('view_chain', game = game, id = curr_id))
    return render_template('chain.html', game_id = curr_id, plaintext_chain = str('\n\n\n'.join(app.games[curr_id].blocks)), game = app.games[curr_id])

@app.route('/get_block/<game>/<game_id>/<block_num>')
def view_block(game, id):
    return render_template('block.html')

if __name__ == '__main__':
    app._static_folder = 'static'
    app.run(host = '0.0.0.0', debug = False, port = WEBAPP_PORT)
