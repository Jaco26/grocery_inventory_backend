from flask_sqlalchemy import SQLAlchemy, Model

class BaseModel(Model):
  def cols_dict(self):
    return { column.name: getattr(self, column.name) for column in self.__table__.columns }


db = SQLAlchemy(model_class=BaseModel)
