from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from game_logic import NavalBattleGame
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), nullable=False)
    board_size = db.Column(db.Integer, default=10, nullable=False)
    shots = db.relationship('Shot', backref='game', lazy=True)

class Shot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    x_coordinate = db.Column(db.Integer, nullable=False)
    y_coordinate = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    shot_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()

game = NavalBattleGame(board_size=10)

@app.route('/')
def index():
    new_game = Game(status='in_progress', board_size=10)
    db.session.add(new_game)
    db.session.commit()
    
    return render_template('index.html', board=game.display_board())

@app.route('/play', methods=['POST'])
def play():
    y = int(request.form.get('x')) - 1  # Заменены местами
    x = int(request.form.get('y')) - 1  # Заменены местами

    result = game.shoot(x, y)

    current_game = Game.query.order_by(Game.id.desc()).first()
    shot = Shot(
        game_id=current_game.id,
        x_coordinate=x,
        y_coordinate=y,
        result='hit' if result.startswith('Попадание') else 'miss'
    )
    db.session.add(shot)
    db.session.commit()

    if game.is_game_over():
        current_game.status = 'completed'
        current_game.end_time = datetime.utcnow()
        current_game.duration = (current_game.end_time - current_game.start_time).seconds
        db.session.commit()

    return jsonify({
        'result': result,
        'board': game.display_board(reveal=False),  # Изменено на reveal=False
        'game_over': game.is_game_over()
    })

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = NavalBattleGame(board_size=10)

    current_game = Game.query.order_by(Game.id.desc()).first()
    if current_game and current_game.status == 'in_progress':
        current_game.status = 'abandoned'
        current_game.end_time = datetime.utcnow()
        current_game.duration = (current_game.end_time - current_game.start_time).seconds
        db.session.commit()

    new_game = Game(status='in_progress', board_size=10)
    db.session.add(new_game)
    db.session.commit()

    return jsonify({
        'board': game.display_board(),
        'result': "Игра начата заново!"
    })

if __name__ == '__main__':
    app.run(debug=True)
