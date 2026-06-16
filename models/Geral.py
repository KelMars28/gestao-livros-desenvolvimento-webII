from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Conecta no MySQL local do XAMPP no banco 'biblioteca'
engine = create_engine("mysql+pymysql://root:@localhost/biblioteca", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)