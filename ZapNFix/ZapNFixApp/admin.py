from django.contrib import admin

from .models import Repair
from .models import User
from .models import Type
from .models import Brand
from .models import Component
from .models import Problem


# Register your models here.
admin.site.register(Repair)
admin.site.register(User)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Component)
admin.site.register(Problem)