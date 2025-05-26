from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from datetime import datetime
from bson import ObjectId
from backend.scraping import obtener_consejos_habitos

from backend.schemas import UserCreate, UserLogin, Token, HabitCreate, HabitUpdate, HabitInDB
from backend.auth import hash_password, verify_password, create_token, decode_token
from backend.database import db

app = FastAPI(
    title="EcoTrack API",
    description="API para registro y gestión de hábitos ecológicos con autenticación JWT.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción a los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_doc(doc):
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        doc.pop("_id")
    return doc


@app.get(
    "/",
    tags=["General"],
    summary="Mensaje de bienvenida",
    response_description="Mensaje simple"
)
async def root():
    """
    Mensaje de bienvenida para comprobar que la API está corriendo.
    """
    return {"mensaje": "Bienvenido a EcoTrack API"}


@app.post(
    "/register",
    tags=["Usuarios"],
    summary="Registrar nuevo usuario",
    response_description="Usuario registrado exitosamente",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Usuario registrado"},
        400: {"description": "Correo ya registrado"},
    },
)
async def register(user: UserCreate):
    """
    Registra un nuevo usuario con email y contraseña.

    - **email**: correo electrónico válido y único
    - **password**: contraseña del usuario
    """
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    new_user = {
        "email": user.email,
        "hashed_password": hash_password(user.password)
    }
    result = await db["users"].insert_one(new_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"mensaje": "Usuario registrado", "user_id": str(result.inserted_id)}
    )


@app.post(
    "/login",
    tags=["Usuarios"],
    summary="Iniciar sesión y obtener token",
    response_model=Token,
    responses={
        200: {"description": "Token generado correctamente"},
        401: {"description": "Credenciales inválidas"},
    },
)
async def login(user: UserLogin):
    """
    Autentica un usuario y genera un token JWT.

    - **email**: correo electrónico registrado
    - **password**: contraseña correspondiente
    """
    db_user = await db["users"].find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token mal formado")
    token = authorization.split(" ")[1]
    email = decode_token(token)
    return email


@app.post(
    "/habits",
    tags=["Hábitos"],
    summary="Crear un nuevo hábito",
    response_model=HabitInDB,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Hábito creado"},
        401: {"description": "No autorizado"},
    },
)
async def create_habit(habit: HabitCreate, email: str = Depends(verify_token)):
    """
    Crea un nuevo hábito asociado al usuario autenticado.

    - **name**: nombre del hábito
    - **frequency**: frecuencia (diaria, semanal, etc.)
    """
    new_habit = habit.dict()
    new_habit["created_at"] = datetime.utcnow()
    new_habit["owner_email"] = email
    result = await db["habits"].insert_one(new_habit)
    inserted_doc = await db["habits"].find_one({"_id": result.inserted_id})
    return serialize_doc(inserted_doc)


@app.get(
    "/habits",
    tags=["Hábitos"],
    summary="Listar hábitos del usuario autenticado",
    response_model=List[HabitInDB],
    responses={
        200: {"description": "Lista de hábitos"},
        401: {"description": "No autorizado"},
    },
)
async def list_habits(email: str = Depends(verify_token)):
    """
    Obtiene todos los hábitos asociados al usuario autenticado.
    """
    habits_cursor = db["habits"].find({"owner_email": email})
    habits = []
    async for habit in habits_cursor:
        habits.append(serialize_doc(habit))
    return habits


@app.put(
    "/habits/{habit_id}",
    tags=["Hábitos"],
    summary="Actualizar un hábito",
    responses={
        200: {"description": "Hábito actualizado"},
        401: {"description": "No autorizado"},
        404: {"description": "Hábito no encontrado"},
    },
)
async def update_habit(habit_id: str, habit: HabitUpdate, email: str = Depends(verify_token)):
    """
    Actualiza los datos de un hábito si pertenece al usuario autenticado.
    """
    existing = await db["habits"].find_one({"_id": ObjectId(habit_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    if existing["owner_email"] != email:
        raise HTTPException(status_code=403, detail="No autorizado")
    update_data = habit.dict()
    await db["habits"].update_one({"_id": ObjectId(habit_id)}, {"$set": update_data})
    return {"mensaje": "Hábito actualizado"}


@app.delete(
    "/habits/{habit_id}",
    tags=["Hábitos"],
    summary="Eliminar un hábito",
    responses={
        200: {"description": "Hábito eliminado"},
        401: {"description": "No autorizado"},
        404: {"description": "Hábito no encontrado"},
    },
)
async def delete_habit(habit_id: str, email: str = Depends(verify_token)):
    """
    Elimina un hábito si pertenece al usuario autenticado.
    """
    existing = await db["habits"].find_one({"_id": ObjectId(habit_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Hábito no encontrado")
    if existing["owner_email"] != email:
        raise HTTPException(status_code=403, detail="No autorizado")
    await db["habits"].delete_one({"_id": ObjectId(habit_id)})
    return {"mensaje": "Hábito eliminado"}

@app.get("/consejos")
async def consejos_habitos():
    consejos = obtener_consejos_habitos()
    return {"consejos": consejos}
