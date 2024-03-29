
from hyp3_db.hyp3_models import Subscription, User, Process
from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_Area, ST_Intersection


def get_users_by_ids(db, user_ids):
    """ Get users from a list of user ids

        :param HyP3DB db: The db to make the query on
        :param list[int] user_ids: User ids to get user objects from

        :returns: hyp3 users with ids in user_ids list
        :rtype: list[hyp3_db.hyp3_models.User]
    """
    user_ids_filter = User.id.in_(user_ids)

    users = db.session.query(User) \
        .filter(user_ids_filter) \
        .all()

    return users


def get_enabled_intersecting_subs(db, polygon, intersection_ratio=0.6):
    """ Get enabled subs intersecting a polygon

        :param HyP3DB db: The db to make the query on
        :param str polygon: WKT polygon

        :returns: hyp3 subscriptions intersecting polygon
        :rtype: list[hyp3_db.hyp3_models.Subscription]
    """
    poly = WKTElement(polygon, srid=4326)

    intersection_area = ST_Area(ST_Intersection(Subscription.location, poly))
    poly_area = ST_Area(poly)

    intersecting_subs = db.session.query(Subscription) \
        .filter_by(enabled=True) \
        .filter(Subscription.process.has(enabled=True)) \
        .filter(Subscription.end_date == None) \
        .filter(intersection_area / poly_area > intersection_ratio) \
        .all()

    return intersecting_subs


def get_processes(db):
    return db.session.query(Process) \
        .all()
