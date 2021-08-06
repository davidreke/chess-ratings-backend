from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import json
from dataclasses import dataclass
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
api = Api(app)

load_dotenv()

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('SQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)


@dataclass
class Player(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    FIDE_Standard = db.Column(db.Integer, nullable=True)
    FIDE_Rapid = db.Column(db.Integer, nullable=True)
    FIDE_Blitz = db.Column(db.Integer, nullable=True)
    USCF_Regular = db.Column(db.Integer, nullable=True)
    USCF_Quick = db.Column(db.Integer, nullable=True)
    USCF_Blitz = db.Column(db.Integer, nullable=True)
    ChessCom_Bullet = db.Column(db.Integer, nullable=True)
    ChessCom_Blitz = db.Column(db.Integer, nullable=True)
    ChessCom_Rapid = db.Column(db.Integer, nullable=True)
    ChessCom_Daily = db.Column(db.Integer, nullable=True)
    ChessCom_Puzzle = db.Column(db.Integer, nullable=True)
    LiChess_Bullet = db.Column(db.Integer, nullable=True)
    LiChess_Blitz = db.Column(db.Integer, nullable=True)
    LiChess_Rapid = db.Column(db.Integer, nullable=True)
    LiChess_Classical = db.Column(db.Integer, nullable=True)
    LiChess_Correspondence = db.Column(db.Integer, nullable=True)
    LiChess_Puzzle = db.Column(db.Integer, nullable=True)

player_post_parser = reqparse.RequestParser()
player_post_parser.add_argument('FIDE', type=dict)
player_post_parser.add_argument('USCF', type=dict)
player_post_parser.add_argument('ChessCom', type = dict)
player_post_parser.add_argument('LiChess', type = dict)

# player_post_args= player_post_parser.parse_args()

FIDE_Parser = reqparse.RequestParser()
FIDE_Parser.add_argument('standard', type= int, location=('nested_one',))
FIDE_Parser.add_argument('rapid', type= int, location=('nested_one',))
FIDE_Parser.add_argument('blitz', type= int, location=('nested_one',))
# FIDE_args = FIDE_Parser.parse_args(req=player_post_args)

USCF_Parser = reqparse.RequestParser()
USCF_Parser.add_argument('regular', type=int, location=('nested_two',))
USCF_Parser.add_argument('quick', type=int, location=('nested_two',))
USCF_Parser.add_argument('blitz', type=int, location=('nested_two',))
# USCF_args = USCF_Parser.parse_args(req=player_post_args)

ChessCom_Parser = reqparse.RequestParser()
ChessCom_Parser.add_argument('bullet', type = int, location=('nexted_three',))
ChessCom_Parser.add_argument('blitz', type = int, location=('nexted_three',))
ChessCom_Parser.add_argument('rapid', type = int, location=('nexted_three',))
ChessCom_Parser.add_argument('daily', type = int, location=('nexted_three',))
ChessCom_Parser.add_argument('puzzle', type = int, location=('nexted_three',))
# ChessCom_args=ChessCom_Parser.parse_args(req=player_post_args)

LiChess_Parser = reqparse.RequestParser()
LiChess_Parser.add_argument('bullet', type = int, location=('nexted_four',))
LiChess_Parser.add_argument('blitz', type = int, location=('nexted_four',))
LiChess_Parser.add_argument('rapid', type = int, location=('nexted_four',))
LiChess_Parser.add_argument('classical', type = int, location=('nexted_four',))
LiChess_Parser.add_argument('correspondence', type = int, location=('nexted_four',))
LiChess_Parser.add_argument('puzzle', type = int, location=('nexted_four',))

player_delete_parser = reqparse.RequestParser()
player_delete_parser.add_argument('id', type=int)


with app.app_context():
    db.create_all()

   

class Players(Resource):
    def get(self):
        result =Player.query.all()
        player_list=[]
        for player in result:
            new_player={'FIDE':{
                'standard':player.FIDE_Standard,
                'rapid':player.FIDE_Rapid,
                'blitz':player.FIDE_Blitz
            },
            'USCF':{
                'regular':player.USCF_Regular,
                'quick':player.USCF_Quick,
                'blitz':player.USCF_Blitz
            },
            'ChessCom':{
                'bullet':player.ChessCom_Bullet,
                'blitz': player.ChessCom_Blitz,
                'rapid':player.ChessCom_Rapid,
                'daily':player.ChessCom_Daily,
                'puzzle':player.ChessCom_Puzzle
            },
            'LiChess':{
                'bullet':player.LiChess_Bullet, 
                'blitz':player.LiChess_Blitz, 
                'rapid':player.LiChess_Rapid, 
                'classical':player.LiChess_Classical, 
                'correspondence':player.LiChess_Correspondence, 
                'puzzle':player.LiChess_Puzzle
            }
            }
            player_list.append(new_player)
            
        return jsonify(player_list)
    def post(self):
        player_post_args = player_post_parser.parse_args()
        FIDE_args=FIDE_Parser.parse_args(req=player_post_args)
        USCF_args=USCF_Parser.parse_args(req=player_post_args)
        ChessCom_args=ChessCom_Parser.parse_args(req=player_post_args)
        LiChess_args=LiChess_Parser.parse_args(req=player_post_args)


        player= Player(
        FIDE_Standard= player_post_args['FIDE']['standard'],
        FIDE_Rapid=player_post_args['FIDE']['rapid'],
        FIDE_Blitz=player_post_args['FIDE']['blitz'],
        USCF_Regular=player_post_args['USCF']['regular'],
        USCF_Quick=player_post_args['USCF']['quick'],
        USCF_Blitz=player_post_args['USCF']['blitz'],
        ChessCom_Bullet=player_post_args['ChessCom']['bullet'],
        ChessCom_Blitz=player_post_args['ChessCom']['blitz'],
        ChessCom_Rapid=player_post_args['ChessCom']['rapid'],
        ChessCom_Daily=player_post_args['ChessCom']['daily'],
        ChessCom_Puzzle=player_post_args['ChessCom']['puzzle'],
        LiChess_Bullet=player_post_args['LiChess']['bullet'],
        LiChess_Blitz=player_post_args['LiChess']['blitz'],
        LiChess_Rapid=player_post_args['LiChess']['rapid'],
        LiChess_Classical=player_post_args['LiChess']['classical'],
        LiChess_Correspondence=player_post_args['LiChess']['correspondence'],
        LiChess_Puzzle=player_post_args['LiChess']['puzzle'],
        )
       
        db.session.add(player)
        db.session.commit()

    def delete(self):
        player_delete_args=player_delete_parser.parse_args()
        id=player_delete_args['id']
        Player.query.filter(Player.id==id).delete()
        db.session.commit()
        return 'player deleted'


api.add_resource(Players, '/players')


if __name__ =="__main__":
    app.run(debug=True)