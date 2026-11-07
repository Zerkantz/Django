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


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer para el registro público de nuevos usuarios.
    - Password con write_only=True y validación de longitud mínima.
    - Validación de confirmación de contraseña opcional si viene enviada.
    """
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password_confirm',
            'telefono',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': False, 'allow_blank': True},
            'telefono': {'required': False, 'allow_blank': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        return value

    def validate(self, attrs):
        pw = attrs.get('password')
        pw_confirm = attrs.get('password_confirm')
        if pw_confirm and pw != pw_confirm:
            raise serializers.ValidationError({"password_confirm": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        user = User.objects.create_user(password=password, **validated_data)
        return user
