from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    mimetype = Column(String(100), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    upload_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Image(id={self.id}, filename={self.filename}, mimetype={self.mimetype}, upload_date={self.upload_date})>"
