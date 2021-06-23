import os
import datetime

from pymongo import MongoClient, ASCENDING
from typing import List, Optional, Union

DATE_FORMAT = "%Y-%m-%d"
DB_USER = os.environ.get("MONGO_DB_USER")
DB_PASSWORD = os.environ.get("MONGO_DB_PASSWORD")


class ROTIMapDB:

  def __init__(self, user: str, password: str):
    client = MongoClient(f"mongodb+srv://{user}:{password}@Cluster0.9nhgn.mongodb.net/igs_roti_db?retryWrites=true&w=majority")
    self.collection = client.igs_roti_db.map

  def date2str(self, date: Union[str, datetime.date]) -> str:
    if isinstance(date, datetime.date):
      date = date.strftime(DATE_FORMAT)
    return date

  def save_map(self, date: Union[str, datetime.date], png_data: str) -> None:
    self.collection.insert_one({
      "date": self.date2str(date),
      "png_data": png_data
    })

  def get_map(self, date: Union[int, datetime.date]) -> Optional[dict]:
    return self.collection.find_one({"date": self.date2str(date)}, {"png_data": 1, "_id": 0})

  def get_dates(self) -> List[dict]:
    return list(self.collection.find({}, {"date": 1, "_id": 0}).sort("date", ASCENDING))


db = ROTIMapDB(DB_USER, DB_PASSWORD)
