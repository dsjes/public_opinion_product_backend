from django.contrib import admin
from .models import ClientUser, Member, Plan, HashUserPassword


class ClientUserAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "line_user_id",
        "email",
        "phone",
        "line_token",
        "displayable",
        "enabled",
        "permission",
        "is_contact",
        "create_time",
        "get_member_name",
    )

    def get_member_name(self, obj):
        return obj.member.name


class MemberAdmin(admin.ModelAdmin):
    list_display = ("uid", "uuid", "name", "plan", "create_time", "enabled")


class PlanAdmin(admin.ModelAdmin):
    list_display = ["plan"]


class HashpasswordAdmin(admin.ModelAdmin):
    list_display = ("user_id", "hashed_password", "only_once", "enabled")


admin.site.register(ClientUser, ClientUserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(HashUserPassword, HashpasswordAdmin)
