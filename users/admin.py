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

from users.models import ContactUs, Statement_1
from users.models import Statement_2
from users.models import Statement_3
from users.models import Statement_4
from users.models import SideChallenge


admin.site.register(Statement_1)
admin.site.register(Statement_2)
admin.site.register(Statement_3)
admin.site.register(Statement_4)
admin.site.register(SideChallenge)
admin.site.register(ContactUs)