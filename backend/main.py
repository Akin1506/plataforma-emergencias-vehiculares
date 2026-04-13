from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    UsuarioRegistro,
    LoginRequest,
    Vehiculo,
    Taller,
    Incidente,
    AsignacionTaller,
    ActualizarEstado,
)
from database import usuarios, vehiculos, talleres, incidentes

app = FastAPI(title="API de Emergencias Vehiculares")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {"mensaje": "API de emergencias vehiculares funcionando"}


# =========================
# USUARIOS / LOGIN
# =========================
@app.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro):
    for u in usuarios:
        if u["correo"] == usuario.correo:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "password": usuario.password,
        "rol": usuario.rol,
    }

    usuarios.append(nuevo_usuario)
    return {"mensaje": "Usuario registrado correctamente", "usuario": nuevo_usuario}


@app.post("/login")
def login(datos: LoginRequest):
    for usuario in usuarios:
        if usuario["correo"] == datos.correo and usuario["password"] == datos.password:
            return {
                "mensaje": "Inicio de sesión exitoso",
                "usuario": {
                    "id": usuario["id"],
                    "nombre": usuario["nombre"],
                    "correo": usuario["correo"],
                    "rol": usuario["rol"],
                },
            }

    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


@app.get("/usuarios")
def listar_usuarios():
    return usuarios


# =========================
# VEHICULOS
# =========================
@app.post("/vehiculos")
def registrar_vehiculo(vehiculo: Vehiculo):
    nuevo_vehiculo = {
        "id": len(vehiculos) + 1,
        "usuario_id": vehiculo.usuario_id,
        "placa": vehiculo.placa,
        "marca": vehiculo.marca,
        "modelo": vehiculo.modelo,
        "color": vehiculo.color,
        "anio": vehiculo.anio,
    }

    vehiculos.append(nuevo_vehiculo)
    return {"mensaje": "Vehículo registrado correctamente", "vehiculo": nuevo_vehiculo}


@app.get("/vehiculos")
def listar_vehiculos():
    return vehiculos


# =========================
# TALLERES
# =========================
@app.post("/talleres")
def registrar_taller(taller: Taller):
    nuevo_taller = {
        "id": len(talleres) + 1,
        "nombre": taller.nombre,
        "ubicacion": taller.ubicacion,
        "especialidad": taller.especialidad,
    }

    talleres.append(nuevo_taller)
    return {"mensaje": "Taller registrado correctamente", "taller": nuevo_taller}


@app.get("/talleres")
def listar_talleres():
    return talleres


# =========================
# INCIDENTES
# =========================
@app.get("/incidentes")
def obtener_incidentes():
    return incidentes


@app.post("/incidentes")
def crear_incidente(incidente: Incidente):
    nuevo_incidente = {
        "id": len(incidentes) + 1,
        "descripcion": incidente.descripcion,
        "ubicacion": incidente.ubicacion,
        "tipo": incidente.tipo,
        "prioridad": incidente.prioridad,
        "estado": "pendiente",
        "taller": None,
    }

    incidentes.append(nuevo_incidente)

    return {
        "mensaje": "Incidente registrado correctamente",
        "incidente": nuevo_incidente,
    }


@app.put("/incidentes/{id}/asignar")
def asignar_taller(id: int, datos: AsignacionTaller):
    for incidente in incidentes:
        if incidente["id"] == id:
            incidente["taller"] = datos.taller
            incidente["estado"] = "asignado"
            return {
                "mensaje": "Taller asignado correctamente",
                "incidente": incidente,
            }

    raise HTTPException(status_code=404, detail="Incidente no encontrado")


@app.put("/incidentes/{id}/estado")
def actualizar_estado(id: int, datos: ActualizarEstado):
    for incidente in incidentes:
        if incidente["id"] == id:
            incidente["estado"] = datos.estado
            return {
                "mensaje": "Estado actualizado correctamente",
                "incidente": incidente,
            }

    raise HTTPException(status_code=404, detail="Incidente no encontrado")