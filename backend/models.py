from pydantic import BaseModel


class UsuarioRegistro(BaseModel):
    nombre: str
    correo: str
    password: str
    rol: str


class LoginRequest(BaseModel):
    correo: str
    password: str


class Vehiculo(BaseModel):
    usuario_id: int
    placa: str
    marca: str
    modelo: str
    color: str
    anio: int


class Taller(BaseModel):
    nombre: str
    ubicacion: str
    especialidad: str


class Incidente(BaseModel):
    descripcion: str
    ubicacion: str
    tipo: str
    prioridad: str


class AsignacionTaller(BaseModel):
    taller: str


class ActualizarEstado(BaseModel):
    estado: str