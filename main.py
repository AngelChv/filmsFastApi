import uvicorn
from fastapi import FastAPI

from app.routers import users, auth
from database import Base, engine

app = FastAPI(title="API Gestión de películas", description="API para organizar en listas tus películas")

app.include_router(users.router)
app.include_router(auth.router)

# Crear las tablas en la base de datos cogiendo las definiciones de models.
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)


# Docs
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc