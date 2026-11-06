from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User personalizado.
    
    Corrección de seguridad 1 del manual:
    - 'password' está configurado con write_only=True. NUNCA se serializa ni
      se expone en respuestas GET, POST, PUT, PATCH ni en /api/v1/auth/me/.
    - Incorpora el campo extra 'telefono' para que aparezca en el serializer y en Swagger.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'telefono',
            'password',
            'is_active',
            'is_staff',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'required': False, 'allow_null': True, 'allow_blank': True},
            'telefono': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
