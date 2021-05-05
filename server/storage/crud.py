from sqlalchemy.orm import Session

from server.storage import models


def get_regions(db: Session):
    return db.query(models.TrackingRegion).all()


def add_region(db: Session, state_id: str, district_id: str):
    region = models.TrackingRegion(state_id=state_id, district_id=district_id)

    db.add(region)
    db.commit()
    db.refresh(region)

    return region


def add_subscription(db: Session, slack_id: str, state_id: str, district_id: str):
    region = (
        db.query(models.TrackingRegion)
        .filter_by(state_id=state_id, district_id=district_id)
        .one_or_none()
    )
    if region is None:
        region = add_region(db, state_id, district_id)

    # Check if user is already subscribed to this region
    for subscription in region.subscriptions:
        if subscription.slack_id == slack_id:
            return subscription

    subscription = models.SlackUserSubscription(slack_id=slack_id, region_id=region.id)

    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return subscription


def add_age_filter(db: Session, slack_id: str, min_age: str):
    user_filter = (
        db.query(models.SlackUserFilters).filter_by(slack_id=slack_id, min_age=min_age).one_or_none()
    )
    if user_filter:
        return user_filter
    user_filters = models.SlackUserFilters(slack_id=slack_id, min_age=min_age)
    db.add(user_filters)
    db.commit()
    db.refresh(user_filters)

    return user_filters


def remove_subscriptions(db: Session, slack_id: str):
    db.query(models.SlackUserSubscription).filter_by(slack_id=slack_id).delete()
    db.commit()


def get_filters_by_slack_id(db: Session, slack_id: str):
    return db.query(models.SlackUserFilters).filter_by(slack_id=slack_id).one_or_none()