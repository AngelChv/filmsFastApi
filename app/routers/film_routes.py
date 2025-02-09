from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.schemas.film_schemas import FilmResponse, FilmCreate, FilmUpdate
from app.services import film_service
from database import get_db

router = APIRouter(prefix="/films", tags=["Películas"])


@router.get("/countAll", response_model=int)
def count_films(db: Session = Depends(get_db)):
    try:
        return film_service.count(db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular el número de películas: {str(e)}")


# Importante! en Depends(get_db) es solo get_db no get_db().
@router.get("/", response_model=List[FilmResponse])
def get_films(db: Session = Depends(get_db)):
    try:
        return film_service.get_films(db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener las películas: {str(e)}")


@router.get("/{film_id}", response_model=FilmResponse | None)
def find_by_id(film_id: int, db: Session = Depends(get_db)):
    try:
        return film_service.find_by_id(film_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener las películas: {str(e)}")


@router.post("/create", response_model=int)
def create_film(film: FilmCreate, db: Session = Depends(get_db)):
    try:
        return film_service.create_film(film, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la película: {str(e)}")


@router.post("/update", response_model=bool)
def update_film(film: FilmUpdate, db: Session = Depends(get_db)):
    try:
        return film_service.update_film(film, db) is not None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la película: {str(e)}")


@router.delete("/{film_id}", response_model=bool)
def delete_film(film_id: int, db: Session = Depends(get_db)):
    try:
        return film_service.delete_film(film_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la película: {str(e)}")
