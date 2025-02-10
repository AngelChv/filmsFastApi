from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.schemas.list_schemas import ListResponse, ListCreate, ListUpdate
from app.services import list_service, film_service
from auth import oauth2_scheme, verify_token
from database import get_db

router = APIRouter(prefix="/lists", tags=["Listas"])


# Importante! en Depends(get_db) es solo get_db no get_db().
@router.get("/{user_id}", response_model=List[ListResponse])
def find_all_by_user_id(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user = film_service.find_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return list_service.find_all_by_user_id(user_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener las listas: {str(e)}")


@router.post("/create", response_model=int)
def create_film(list_create: ListCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user = film_service.find_by_id(list_create.user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return list_service.create_list(list_create, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la lista: {str(e)}")


@router.post("/update", response_model=bool)
def update_list(list_update: ListUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        return list_service.update_list(list_update, db) is not None
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la lista: {str(e)}")


@router.delete("/{list_id}", response_model=bool)
def delete_film(list_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        return list_service.delete_list(list_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la lista: {str(e)}")


@router.post("/add_film/{list_id}/{film_id}", response_model=bool)
def add_film(list_id: int, film_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        return list_service.add_film_to_list(list_id, film_id, db)
    except IntegrityError as ie:
        if "UNIQUE constraint failed" in str(ie.orig):
            raise HTTPException(
                status_code=400,
                detail="La película ya está en la lista"
            )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al añadir la película a la lista: {str(e)}")


@router.delete("/remove_film/{list_id}/{film_id}", response_model=bool)
def add_film(list_id: int, film_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        return list_service.remove_film_from_list(list_id, film_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la película de la lista: {str(e)}")


@router.get("/count_all_of_user/{user_id}", response_model=int)
def count_all_of_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> int:
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        return list_service.count_all_of_user(user_id, db)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener el calculo de listas: {str(e)}")
