import sqlalchemy as sa
import sqlalchemy.orm as orm
from flask.ext.login import UserMixin
from sqlalchemy_login_models.model import Base, UserKey, User as SLM_User


__all__ = ['Coin']


class Coin(Base):
    """A Coin for someone's collection."""
    __tablename__ = "coin"
    __name__ = "coin"

    id = sa.Column(sa.Integer, primary_key=True, doc="primary key")
    metal = sa.Column(sa.String(255), nullable=False)
    mint = sa.Column(sa.String(255), nullable=False)

    # foreign key reference to the owner of this coin's API key
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('user.id'),
        nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])

    def __init__(self, metal, mint, uid):
        self.metal = metal
        self.mint = mint
        self.user_id = uid

