from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- Usuario ---

class UserCreate(BaseModel):
    email: EmailStr = Field(..., example="usuario@ejemplo.com")
    password: str = Field(..., example="contraseña123")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., example="usuario@ejemplo.com")
    password: str = Field(..., example="contraseña123")

class Token(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")

# --- Hábitos ---

class HabitBase(BaseModel):
    name: str = Field(..., example="Ejercicio")
    frequency: str = Field(..., example="diaria")  # "diaria", "semanal", etc.

class HabitCreate(HabitBase):
    pass

class HabitUpdate(HabitBase):
    pass

class HabitInDB(HabitBase):
    id: Optional[str] = Field(None, example="60f6c2a21f1a256a7f5a4c21")
    owner_email: Optional[str] = Field(None, alias="ownerEmail", example="usuario@ejemplo.com")
    created_at: Optional[datetime] = Field(None, example="2023-05-24T14:30:00Z")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
