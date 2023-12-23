from dataclasses import dataclass
from typing import Dict, Any, Iterable
from pandas import DataFrame
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
import urllib
import datetime

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base,mapped_column,Mapped,sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

class Credit(Base):
     __tablename__ = "user_account"
     Id = Column(Integer, primary_key=True)
     Job = Column(Integer)
     Housing = Column(String)

     SavingAccounts = relationship(
         "Address", back_populates="user", cascade="all, delete-orphan"
     )

     def __repr__(self):
         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
@dataclass(frozen=True)
class ConnectionSettings:
    """Connection Settings."""
    server: str
    database: str
    username: str
    password: str
    driver: str
    timeout: int = 30

class AzureDbConnection:
    """
    Azure SQL database connection.
    """
    def __init__(self, conn_settings: ConnectionSettings, echo: bool = False) -> None:
        conn_params = urllib.parse.quote_plus(
            'Driver=%s;' % conn_settings.driver +
            'Server=tcp:%s.database.windows.net,1433;' % conn_settings.server +
            'Database=%s;' % conn_settings.database +
            'Uid=%s;' % conn_settings.username +
            'Pwd=%s;' % conn_settings.password +
            'Encrypt=yes;' +
            'TrustServerCertificate=no;' +
            'Connection Timeout=%s;' % conn_settings.timeout
        )
        conn_string = f'mssql+pyodbc:///?odbc_connect={conn_params}'

        self.db = create_engine(conn_string, echo=echo)

    def connect(self) -> None:
        """Estimate connection."""
        self.conn = self.db.connect()
        return self.conn
    
    def engine(self):
        return self.db
    def sessionMaker(self):
        session = sessionmaker(bind=self.db)
        return session()
    def session(self):
        return Session(self.db)
    
    def show_records(self):
        records = self.db.all()
        return records
    
    def get_tables(self) -> Iterable[str]:
        """Get list of tables."""
        inspector = inspect(self.db)
        return [t for t in inspector.get_table_names()]

    def dispose(self) -> None:
        """Dispose opened connections."""
        self.conn.close()
        self.db.dispose()

# class Credit(Base):
#     __tablename__ = "Credit"
    
#     Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
#     Job: Mapped[int] = mapped_column()
#     Housing: Mapped[str] = mapped_column()
#     SavingAccounts: Mapped[str] = mapped_column()
#     CheckingAccount: Mapped[str] = mapped_column()
#     CreditAmount: Mapped[str] = mapped_column()
#     Duration: Mapped[int] = mapped_column()
#     Purpose: Mapped[str] = mapped_column()

# class Heart(Base):
#     __tablename__ = "Heart"
    
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
#     age: Mapped[int] = mapped_column()
#     sex: Mapped[str] = mapped_column()
#     dataset: Mapped[str] = mapped_column()
#     cp: Mapped[str] = mapped_column()
#     trestbps: Mapped[float] = mapped_column()
#     chol: Mapped[float] = mapped_column()
#     fbs: Mapped[bool] = mapped_column()
#     restecg: Mapped[str] = mapped_column()
#     thalch: Mapped[float] = mapped_column()
#     exang: Mapped[bool] = mapped_column()
#     oldpeak: Mapped[float] = mapped_column()
#     slope: Mapped[str] = mapped_column()
#     ca: Mapped[float] = mapped_column()
#     thal: Mapped[str] = mapped_column()
#     num: Mapped[int] = mapped_column()

# class Insurance(Base):
#     __tablename__ = "Insurance"
    
#     Id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
#     bmi: Mapped[float] = mapped_column()
#     children: Mapped[int] = mapped_column()
#     smoker: Mapped[str] = mapped_column()
#     region: Mapped[str] = mapped_column()
#     charges: Mapped[float] = mapped_column()

