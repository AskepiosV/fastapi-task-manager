from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Tarea(BaseModel):
    tarea: str

def cargarTareas():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardarTareas(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

tasks = cargarTareas()

@app.get("/tareas")
def ver_tareas():
    return tasks

@app.post("/tareas")
def agregar_tarea(tarea: Tarea):
    nueva = {"tarea": tarea.tarea, "completada": False}
    tasks.append(nueva)
    guardarTareas(tasks)
    return {"mensaje": "Tarea agregada", "tarea": nueva}


@app.put("/tareas/{id}")
def completar_tarea(id: int):
    if id < 0 or id >= len(tasks):
        return {"error": "ID no válido"}

    tasks[id]["completada"] = True
    guardarTareas(tasks)
    return {"mensaje": "Tarea completada"}


@app.put("/tareas/{id}/editar")
def editar_tarea(id: int, tarea: Tarea):
    if id < 0 or id >= len(tasks):
        return {"error": "ID no válido"}

    tasks[id]["tarea"] = tarea.tarea
    guardarTareas(tasks)
    return {"mensaje": "Tarea actualizada"}


@app.delete("/tareas/{id}")
def eliminar_tarea(id: int):
    if id < 0 or id >= len(tasks):
        return {"error": "ID no válido"}

    tarea_eliminada = tasks.pop(id)
    guardarTareas(tasks)
    return {"mensaje": "Tarea eliminada", "tarea": tarea_eliminada}
