from fastapi import FastAPI, HTTPException
from models import (
    IntegranteBase, Integrante,
    AlbumBase, Album, AlbumUpdate,
    TourBase, Tour
)
from db import SessionDep, create_all_tables
from operations_bts import (
    crear_integrante, ver_integrantes, buscar_integrante_nombre,
    crear_album, ver_albumes, buscar_album_id, editar_album,
    crear_tour, ver_tours, buscar_tours_en_ciudad, cancelar_tour
)

app = FastAPI(lifespan=create_all_tables)

#ENDPOINTS INTEGRANTES BTS

@app.post("/integrantes", response_model=Integrante, tags=["Integrantes"])
async def Crea_Tu_Integrante(integrante: IntegranteBase, session: SessionDep):
    return crear_integrante(integrante, session)

@app.get("/integrantes", response_model=list[Integrante], tags=["Integrantes"])
async def Ver_Integrantes(session: SessionDep):
    return ver_integrantes(session)

@app.get("/integrantes/buscar/{nombre}", response_model=list[Integrante], tags=["Integrantes"])
async def Buscar_Integrante_Nombre(nombre: str, session: SessionDep):
    resultados = buscar_integrante_nombre(nombre, session)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontró ningún integrante con nombre '{nombre}'")
    return resultados

#ENDPOINTS ÁLBUMES BTS

@app.post("/albumes", response_model=Album, tags=["Álbumes"])
async def Crear_Album(album: AlbumBase, session: SessionDep):
    return crear_album(album, session)

@app.get("/albumes", response_model=list[Album], tags=["Álbumes"])
async def Ver_Albumes(session: SessionDep):
    return ver_albumes(session)

@app.get("/albumes/{id}", response_model=Album, tags=["Álbumes"])
async def Buscar_AlbumID(id: int, session: SessionDep):
    album = buscar_album_id(id, session)
    if not album:
        raise HTTPException(status_code=404, detail=f"Álbum con ID {id} no encontrado")
    return album

@app.patch("/albumes/{id}", response_model=Album, tags=["Álbumes"])
async def Edita_Albumes(id: int, datos: AlbumUpdate, session: SessionDep):
    album = editar_album(id, datos, session)
    if not album:
        raise HTTPException(status_code=404, detail=f"Álbum con ID {id} no encontrado")
    return album

#ENDPOINTS TOURS BTS

@app.post("/tours", response_model=Tour, tags=["Tours"])
async def Crear_Tour(tour: TourBase, session: SessionDep):
    return crear_tour(tour, session)

@app.get("/tours", response_model=list[Tour], tags=["Tours"])
async def Ver_Tours(session: SessionDep):
    return ver_tours(session)

@app.get("/tours/buscar/{ciudad}", response_model=list[Tour], tags=["Tours"])
async def Buscar_Tours_En_Ciudad(ciudad: str, session: SessionDep):
    resultados = buscar_tours_en_ciudad(ciudad, session)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron tours en la ciudad '{ciudad}'")
    return resultados

@app.delete("/tours/{id}", response_model=Tour, tags=["Tours"])
async def Cancelar_Tour(id: int, session: SessionDep):
    tour = cancelar_tour(id, session)
    if not tour:
        raise HTTPException(status_code=404, detail=f"Tour con ID {id} no encontrado")
    return tour

#RAÍZ

@app.get("/")
async def root():
    return {"message": "MEET BTS"}