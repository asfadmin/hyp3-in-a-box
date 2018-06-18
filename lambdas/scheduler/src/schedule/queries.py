
from hyp3_db.hyp3_models import Subscription, User
from geoalchemy2 import WKTElement


def get_users_by_ids(db, user_ids):
    """ Get users from a list of user ids

        :param Hyp3DB db: The db to make the query on
        :param list[int] user_ids: User ids to get user objects from

        :returns: hyp3 users with ids in user_ids list
        :rtype: list[hyp3_db.hyp3_models.User]
    """
    user_ids_filter = User.id.in_(user_ids)

    users = db.session.query(User) \
        .filter(user_ids_filter) \
        .all()

    return users


def get_enabled_containing_subs(db, polygon):
    poly = WKTElement(polygon, srid=4326)
    intersection = Subscription.location.ST_Intersects(poly)

    intersecting_subs = enabled_subs_query(db) \
        .filter(intersection) \
        .all()

    return intersecting_subs


def enabled_subs_query(db):
    return db.session.query(Subscription) \
        .filter_by(enabled=True)
