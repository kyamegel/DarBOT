from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Change the connection string as needed
DATABASE_URL = "sqlite:///bosses.db"
# For MySQL e.g.: "mysql+pymysql://user:pass@localhost/dbname"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Boss(Base):
    __tablename__ = "bosses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    spawn_datetime = Column(DateTime)
    otod = Column(String(50))
    ntod = Column(String(200))
    timer = Column(Text)
    metadata = Column(Text)

def create_db():
    Base.metadata.create_all(engine)

def seed_data(session, boss_list):
    for b in boss_list:
        dt = None
        if "spawn_datetime" in b and b["spawn_datetime"]:
            dt = datetime.datetime.fromisoformat(b["spawn_datetime"])
        boss = Boss(
            level=b["level"],
            name=b["name"],
            spawn_datetime=dt,
            otod=b.get("otod"),
            ntod=b.get("ntod"),
            timer=b.get("timer"),
            metadata=b.get("metadata"),
        )
        session.add(boss)
    session.commit()

if __name__ == "__main__":
    create_db()
    session = Session()
    boss_list = [
        {
            "level": 60,
            "name": "Venatus",
            "spawn_datetime": "2025-10-10 17:48:00",
            "otod": "10",
            "ntod": "7:48<t:1760089680:R>###",
            "timer": "- *``60``* Venatus (*10hrs*) <t:1760089680:R>",
            "metadata": None
        },
        {
            "level": 65,
            "name": "Viorent",
            "spawn_datetime": "2025-10-10 17:52:00",
            "otod": "10",
            "ntod": "7:52<t:1760089920:R>###",
            "timer": "- *``65``* Viorent (*10hrs*) <t:1760089920:R>",
            "metadata": None
        },
        # Add others...
    ]
    seed_data(session, boss_list)
    print(session.query(Boss).all())
