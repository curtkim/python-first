from typing import Optional
from sqlmodel import Field, SQLModel
from sqlmodel import create_engine, Session, select


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


hero1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero2 = Hero(name="Spider-Bod", secret_name="Pedro Parqueador")
hero3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero1)
    session.add(hero2)
    session.add(hero3)
    session.commit()

with Session(engine) as session:
    stmt = select(Hero).where(Hero.name == "Spider-Bod")
    hero = session.exec(stmt).first()
    print(hero.name)

