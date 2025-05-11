from flask import Flask, render_template, request, redirect, url_for
from models import db, Tournament, Box, Player
import random
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
app.config['SECRET_KEY'] = 'secret joisdjfiosdjfiosjd'

db.init_app(app)

migrate = Migrate(app, db)



@app.route('/')
def index():
    tournaments = Tournament.query.all()
    return render_template('index.html', tournaments=tournaments)


@app.route('/create/tournament', methods=['GET', 'POST'])
def create_tournament():
    if request.method == 'POST':
        title = request.form.get('title')
        count_players = request.form.get('count')

        if title and count_players:
            tournament = Tournament(title=title, count=int(count_players))
            db.session.add(tournament)
            db.session.commit()
            return redirect(url_for('create_players', id=tournament.id))
        return render_template('create_tournament.html', error="Iltimos, barcha maydonlarni to'ldiring!")

    return render_template('create_tournament.html')


@app.route('/create/players/<int:id>', methods=['GET', 'POST'])
def create_players(id):
    tournament = Tournament.query.get_or_404(id)
    players_count = tournament.count

    if request.method == 'POST':
        names = request.form.getlist('name')
        if len(names) != players_count:
            return render_template('players.html', tournament=tournament, players=players_count, error="Iltimos, kerakli miqdorda o'yinchilarni kiriting!")

        for name in names:
            if name.strip():
                new_player = Player(name=name, tournament_id=id)
                db.session.add(new_player)
        db.session.commit()
        return redirect(url_for('pair_players', id=id))

    return render_template('players.html', tournament=tournament, players=players_count)


@app.route('/random/<int:id>')
def pair_players(id):
    tournament = Tournament.query.get_or_404(id)
    players = Player.query.filter_by(tournament_id=id).all()

    if not players:
        return redirect(url_for('create_players', id=id))

    random.shuffle(players)
    total_players = len(players)
    boxes = []

    # Chorak finallar (4 juftlik, 2 chapda, 2 o'ngda)
    for i in range(0, total_players, 2):
        if i + 1 < total_players:
            pair = Box(
                item1=players[i].name,
                item2=players[i + 1].name,
                tournament_id=id
            )
        else:
            pair = Box(
                item1=players[i].name,
                item2=None,
                tournament_id=id
            )
        boxes.append(pair)

   
    for box in boxes:
        db.session.add(box)
    db.session.commit()

    return redirect(url_for('show_results', tournament_id=id))


@app.route('/tournament/<int:tournament_id>/results')
def show_results(tournament_id):
    tournament = Tournament.query.get_or_404(tournament_id)
    boxes = Box.query.filter_by(tournament_id=tournament_id).all()
    return render_template('result.html', boxes=boxes, tournament=tournament)


if __name__ == '__main__':
	app.run(debug=True)