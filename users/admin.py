from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuración del panel de administración para el modelo User personalizado.
    Muestra el campo extra 'telefono' en la lista y en los formularios de edición y creación.
    """
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'telefono',
        'is_staff',
        'is_active',
    )
    list_display_links = ('id', 'email')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'telefono')
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal', {
            'fields': ('username', 'first_name', 'last_name', 'telefono')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password',
                'username',
                'first_name',
                'last_name',
                'telefono',
                'is_staff',
                'is_active',
            ),
        }),
    )
