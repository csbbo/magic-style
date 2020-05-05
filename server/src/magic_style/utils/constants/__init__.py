class Choices:
    @classmethod
    def choices(cls, *, exclude_field=()):
        d = cls.__dict__
        ret = {str(d[item]) for item in d.keys() if not item.startswith("_")}
        return list(ret - set(exclude_field))
