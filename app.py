from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from dataclasses import dataclass
from flask_cors import CORS
import os

# ---------------------------------------------------------
# App Setup
# ---------------------------------------------------------

app = Flask(__name__)
CORS(app)
api = Api(app)

load_dotenv()

app.config['PROPAGATE_EXCEPTIONS'] = True

# ---------------------------------------------------------
# Database Configuration
# ---------------------------------------------------------

db_url = os.environ.get("SQL_URI")

# Normalize old Heroku URLs (postgres:// → postgresql://)
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Ensure SSL for Heroku Postgres
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {"sslmode": "require"}
}

db = SQLAlchemy(app)

# ---------------------------------------------------------
# Models
# ---------------------------------------------------------

@dataclass
class Player(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    FIDE_Standard: int = db.Column(db.Integer, nullable=True)
    FIDE_Rapid: int = db.Column(db.Integer, nullable=True)
    FIDE_Blitz: int = db.Column(db.Integer, nullable=True)
    USCF_Regular: int = db.Column(db.Integer, nullable=True)
    USCF_Quick: int = db.Column(db.Integer, nullable=True)
    USCF_Blitz: int = db.Column(db.Integer, nullable=True)
    ChessCom_Bullet: int = db.Column(db.Integer, nullable=True)
    ChessCom_Blitz: int = db.Column(db.Integer, nullable=True)
    ChessCom_Rapid: int = db.Column(db.Integer, nullable=True)
    ChessCom_Daily: int = db.Column(db.Integer, nullable=True)
    ChessCom_Puzzle: int = db.Column(db.Integer, nullable=True)
    LiChess_Bullet: int = db.Column(db.Integer, nullable=True)
    LiChess_Blitz: int = db.Column(db.Integer, nullable=True)
    LiChess_Rapid: int = db.Column(db.Integer, nullable=True)
    LiChess_Classical: int = db.Column(db.Integer, nullable=True)
    LiChess_Correspondence: int = db.Column(db.Integer, nullable=True)
    LiChess_Puzzle: int = db.Column(db.Integer, nullable=True)

# ---------------------------------------------------------
# Parsers
# ---------------------------------------------------------

player_post_parser = reqparse.RequestParser()
player_post_parser.add_argument('FIDE', type=dict)
player_post_parser.add_argument('USCF', type=dict)
player_post_parser.add_argument('ChessCom', type=dict)
player_post_parser.add_argument('LiChess', type=dict)

player_delete_parser = reqparse.RequestParser()
player_delete_parser.add_argument('id', type=int)
player_delete_parser.add_argument('secret', type=str)

# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

@app.route("/")
def home():
    return "Backend is running"

class Players(Resource):
    def get(self):
        players = Player.query.all()
        output = []

        for p in players:
            output.append({
                "FIDE": {
                    "standard": p.FIDE_Standard,
                    "rapid": p.FIDE_Rapid,
                    "blitz": p.FIDE_Blitz
                },
                "USCF": {
                    "regular": p.USCF_Regular,
                    "quick": p.USCF_Quick,
                    "blitz": p.USCF_Blitz
                },
                "ChessCom": {
                    "bullet": p.ChessCom_Bullet,
                    "blitz": p.ChessCom_Blitz,
                    "rapid": p.ChessCom_Rapid,
                    "daily": p.ChessCom_Daily,
                    "puzzle": p.ChessCom_Puzzle
                },
                "LiChess": {
                    "bullet": p.LiChess_Bullet,
                    "blitz": p.LiChess_Blitz,
                    "rapid": p.LiChess_Rapid,
                    "classical": p.LiChess_Classical,
                    "correspondence": p.LiChess_Correspondence,
                    "puzzle": p.LiChess_Puzzle
                }
            })

        return jsonify(output)

    def post(self):
        data = player_post_parser.parse_args()

        player = Player(
            FIDE_Standard=data["FIDE"]["standard"],
            FIDE_Rapid=data["FIDE"]["rapid"],
            FIDE_Blitz=data["FIDE"]["blitz"],
            USCF_Regular=data["USCF"]["regular"],
            USCF_Quick=data["USCF"]["quick"],
            USCF_Blitz=data["USCF"]["blitz"],
            ChessCom_Bullet=data["ChessCom"]["bullet"],
            ChessCom_Blitz=data["ChessCom"]["blitz"],
            ChessCom_Rapid=data["ChessCom"]["rapid"],
            ChessCom_Daily=data["ChessCom"]["daily"],
            ChessCom_Puzzle=data["ChessCom"]["puzzle"],
            LiChess_Bullet=data["LiChess"]["bullet"],
            LiChess_Blitz=data["LiChess"]["blitz"],
            LiChess_Rapid=data["LiChess"]["rapid"],
            LiChess_Classical=data["LiChess"]["classical"],
            LiChess_Correspondence=data["LiChess"]["correspondence"],
            LiChess_Puzzle=data["LiChess"]["puzzle"]
        )

        db.session.add(player)
        db.session.commit()
        return {"message": "Player added"}, 201

    def delete(self):
        args = player_delete_parser.parse_args()
        if args["secret"] != os.environ.get("SECRET"):
            return {"error": "wrong secret"}, 403

        Player.query.filter_by(id=args["id"]).delete()
        db.session.commit()
        return {"message": "player deleted"}

api.add_resource(Players, "/players")

# ---------------------------------------------------------
# Local Dev Entry Point
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
