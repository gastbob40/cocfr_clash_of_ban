import datetime

from src.models.warn import Warn

a = Warn()
a.save()
print(a.id)