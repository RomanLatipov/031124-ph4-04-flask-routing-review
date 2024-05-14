#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Meme # import your models here!

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

@app.post('/api/memes')
def post_rqst():
    new_meme = Meme(img_url=request.json['img_url'], caption=request.json['caption'], likes=request.json['likes'])
    db.session.add(new_meme)
    db.session.commit()
    return new_meme.to_dict(), 201

@app.get('/api/memes')
def get_rqst():
    return [meme.to_dict() for meme in Meme.query.all()]

@app.get('/api/memes/<int:id>')
def get_by_id(id):
    meme = Meme.query.where(Meme.id == id).first()
    if meme:
        return meme.to_dict(), 200
    else:
        return {"error": "Not found"}, 404
    
@app.delete('/api/memes/<int:id>')
def delete_rqst(id):
    meme = Meme.query.where(Meme.id == id).first()
    if meme:
        db.session.delete(meme)
        db.session.commit()
        return {}, 204
    else:
        return {"error": "Not found"}, 404
    
@app.patch("/api/memes/<int:id>")
def patch_rqst(id):
    meme = Meme.query.where(Meme.id == id).first()
    if meme:
        for key in request.json.keys():
            if not key == "id":
                setattr(meme, key, request.json[key])
        
        db.session.add(meme)
        db.session.commit()

        return meme.to_dict(), 202
    
    else:
        return{"error": "Not found"}, 404

    



# write your routes here!

if __name__ == '__main__':
    app.run(port=5555, debug=True)
