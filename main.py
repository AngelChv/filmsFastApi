import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers import users_routes, film_routes, list_routes

from database import Base, engine

app = FastAPI(title="API Gestión de películas", description="API para organizar en listas tus películas")

app.include_router(users_routes.router)
app.include_router(film_routes.router)
app.include_router(list_routes.router)

# Crear las tablas en la base de datos cogiendo las definiciones de models.
Base.metadata.create_all(bind=engine)

# Para que funcione con el cliente de flutter web:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar esto a ["http://localhost:3000"] si solo es para desarrollo ¿?
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Permite todos los encabezados
)

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