#credits: http://piotr.banaszkiewicz.org/blog/2012/06/30/serialize-sqlalchemy-results-into-json/
from collections import OrderedDict

class DictSerializable(object):
	def _asdict(self):
		result = OrderedDict()
		for key in self.__mapper__.c.keys():
			result[key] = getattr(self, key)
		return result