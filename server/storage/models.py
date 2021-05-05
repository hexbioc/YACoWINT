from sqlalchemy import Column, ForeignKey, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from server.storage.session import Base


class TrackingRegion(Base):
    __tablename__ = "tracking_regions"

    id = Column(
        String,
        nullable=False,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    state_id = Column(String, index=True, nullable=False)
    district_id = Column(String, index=True, nullable=False)

    subscriptions = relationship("SlackUserSubscription", back_populates="region")


class SlackUserSubscription(Base):
    __tablename__ = "slack_user_subscriptions"

    id = Column(
        String,
        nullable=False,
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
    )
    slack_id = Column(String, index=True, nullable=False)
    region_id = Column(String, ForeignKey("tracking_regions.id"))

    region = relationship("TrackingRegion", back_populates="subscriptions")


class SlackUserFilters(Base):
    __tablename__ = "slack_user_min_age"
    slack_id = Column(String, primary_key=True, nullable=False)
    min_age = Column(Enum("18", "45", name="user_age_group_types"))
