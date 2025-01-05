import uuid


class Topic:
    PUBLISH = f"/:119746:2432000646/usp/admin/request/reply-to=%2F:119746:2432000646%2Fusp%2Fadmin%2Freply-to%2F"
    SUBSCRIBE = "/:119746:2432000646/usp/admin/reply-to/"

    def __init__(self):
        self.uuid_on = str(uuid.uuid4())
        self.uuid_off = str(uuid.uuid4())
        self.uuid_query = str(uuid.uuid4())

    def __repr__(self):
        return "on:%s\noff:%s\nquery:%s" % (self.uuid_on, self.uuid_off, self.uuid_query)

    def get_publish_on(self):
        return Topic.PUBLISH + self.uuid_on

    def get_subscribe_on(self):
        return Topic.SUBSCRIBE + self.uuid_on

    def get_publish_off(self):
        return Topic.PUBLISH + self.uuid_off

    def get_subscribe_off(self):
        return Topic.SUBSCRIBE + self.uuid_off

    def get_publish_query(self):
        return Topic.PUBLISH + self.uuid_query

    def get_subscribe_query(self):
        return Topic.SUBSCRIBE + self.uuid_query
