from flask.json import JSONEncoder
from sqlalchemy.inspection import inspect


class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class SerializingJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Serializer):
            try:
                return obj.serialize()
            except:
                pass

        return JSONEncoder.default(self, obj)
