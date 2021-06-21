from fastapi import APIRouter, File, UploadFile, HTTPException
from http import HTTPStatus

from .db import db
from .roti import ROTIMap

router = APIRouter()


@router.get("/ping")
def ping():
  return {"msg": "Pong!"}


@router.post("/plot-map")
async def plot_map(file: UploadFile = File(...)):
  roti_map = ROTIMap()
  try:
    await roti_map.read_from_file(file)
  except Exception:
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
  date = roti_map.DATE
  png_data = roti_map.plot()
  if not db.get_map(date):
    db.save_map(date, png_data)
  return {"png_data": png_data}


@router.get("/dates")
def get_dates():
  return db.get_dates()


@router.get("/map")
def get_map(date: str):
  return db.get_map(date)
