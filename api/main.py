from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import schemas
import models

app = FastAPI()
app.mount("/static", StaticFiles(directory="../ui/build/static", check_dir=False), name="static")


@app.get("/")
def serve_react_app():
    return FileResponse("../ui/build/index.html")

# pobieranie filmów
@app.get("/movies", response_model=List[schemas.Movie])
def get_movies():
    return list(models.Movie.select())

#dodanie nowego filmu
@app.post("/movies", response_model=schemas.Movie)
def add_movie(movie: schemas.MovieBase):
    movie = models.Movie.create(**movie.dict())
    return movie

#pobranie konkretnego fimu z aktorami
@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie


#pobieranie aktorów
@app.get("/actors", response_model=List[schemas.Actor])
def get_actors():
    return list(models.Actor.select())

#dodanie nowego aktora
@app.post("/actors", response_model=schemas.Actor)
def add_actor(movie: schemas.ActorCreate):
    actor = models.Actor.create(**actor.dict())
    return actor

#usunięcie aktora
@app.delete("/actors/{actor_id}")
def delete_actor(actor_id: int):
    db_actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if db_actor is None:
        raise HTTPException(status_code=404, detail="Aktor nie istnieje")
    db_actor.delete_instance()
    return {"message": "Aktor usunięty"}

# 🔹 Przypisanie aktora do filmu
@app.post("/movies/{movie_id}/actors/{actor_id}")
def assign_actor_to_movie(movie_id: int, actor_id: int):
    movie = models.Movie.filter(models.Movie.id == movie_id).first()
    actor = models.Actor.filter(models.Actor.id == actor_id).first()
    if not movie or not actor:
        raise HTTPException(status_code=404, detail="Film lub aktor nie istnieje")
    movie.actors.add(actor)
    return {"message": "Aktor przypisany do filmu"}

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def get_movie(movie_id: int):
    db_movie = models.Movie.filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_movie.delete_instance()
    return db_movie
