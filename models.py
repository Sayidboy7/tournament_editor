from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Models
class Tournament(db.Model):
	__tablename__ = 'tournament'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255), nullable=False)
	count = db.Column(db.Integer, default=2)

	players = db.relationship('Player', backref='tournament')
	random_boxes = db.relationship('Box', backref='tournament')

	def __repr__(self):
		return f'{self.title} : {self.count}'


class Box(db.Model):
    __tablename__ = 'boxes'
    id = db.Column(db.Integer, primary_key=True)
    item1 = db.Column(db.String(255))
    item2 = db.Column(db.String(255))
    stage = db.Column(db.String(50))
    side = db.Column(db.String(50))

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))


class Player(db.Model):
	__tablename__ = 'players'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))

	tournament_id = db.Column(db.Integer, db.ForeignKey(Tournament.id))
