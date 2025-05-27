from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export import resources
from import_export.admin import ImportExportModelAdmin

User = get_user_model()

class UserResource(resources.ModelResource):
    class Meta:
        model = User

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = tuple(f.name for f in User._meta.fields if f.name not in ('password', 'is_staff', 'is_superuser'))