from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models import (
    Integrante, IntegranteBase,
    Album, AlbumBase, AlbumUpdate,
    Tour, TourBase
)

#OPERACIONES INTEGRANTES
def crear_integrante(integrante: IntegranteBase, session: Session):
    nuevo = Integrante.model_validate(integrante)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

def ver_integrantes(session: Session):
    return session.exec(select(Integrante)).all()

def buscar_integrante_nombre(nombre: str, session: Session):
    # Búsqueda parcial e insensible a mayúsculas
    statement = select(Integrante).where(Integrante.nombre.ilike(f"%{nombre}%"))
    return session.exec(statement).all()

#OPERACIONES ÁLBUM
def crear_album(album: AlbumBase, session: Session):
    nuevo = Album.model_validate(album)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

def ver_albumes(session: Session):
    return session.exec(select(Album)).all()

def buscar_album_id(id: int, session: Session):
    try:
        return session.get_one(Album, id)
    except NoResultFound:
        return None

def editar_album(id: int, datos: AlbumUpdate, session: Session):
    album = buscar_album_id(id, session)
    if album is None:
        return None
    campos_nuevos = datos.model_dump(exclude_unset=True)
    album.sqlmodel_update(campos_nuevos)
    session.add(album)
    session.commit()
    session.refresh(album)
    return album

#  OPERACIONES TOURS
def crear_tour(tour: TourBase, session: Session):
    nuevo = Tour.model_validate(tour)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

def ver_tours(session: Session):
    return session.exec(select(Tour)).all()

def buscar_tours_en_ciudad(ciudad: str, session: Session):
    # Busca tours que contengan la ciudad (búsqueda parcial)
    statement = select(Tour).where(Tour.ciudades_visitadas.ilike(f"%{ciudad}%"))
    return session.exec(statement).all()

def cancelar_tour(id: int, session: Session):
    try:
        tour = session.get_one(Tour, id)
        session.delete(tour)
        session.commit()
        return tour
    except NoResultFound:
        return None