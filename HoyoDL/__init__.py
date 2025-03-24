import sys
from .main import HoyoDL

class _ModuleWrapper:
	def __call__(self, *args, **kwargs):
		return HoyoDL(*args, **kwargs)

sys.modules[__name__] = _ModuleWrapper()
