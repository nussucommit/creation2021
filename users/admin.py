from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import ChallengeStatus

# Register your models here.
class StatusInLine(admin.StackedInline):
    model = ChallengeStatus
    can_delete = False
    verbose_name_plural = 'status'

class UserAdmin(BaseUserAdmin):
    inlines = (StatusInLine, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)