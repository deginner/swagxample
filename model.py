import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base

SABase = declarative_base()


class Coin(SABase):
    """A Coin for someone's collection."""
    __tablename__ = "coin"
    __name__ = "coin"

    id = sa.Column(sa.Integer, primary_key=True, doc="primary key")
    metal = sa.Column(sa.String(255), nullable=False)
    mint = sa.Column(sa.String(255), nullable=False)

    def __init__(self, metal, mint):
        self.metal = metal
        self.mint = mint
