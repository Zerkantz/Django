from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserApiViewSet(ModelViewSet):
    """
    CRUD completo para la gestión de usuarios (solo administradores).
    
    Correcciones de seguridad respecto al manual:
    1. La contraseña no se expone en ninguna respuesta (write_only=True en UserSerializer).
    2. En update y partial_update, NUNCA se asigna request.user.password cuando no viene contraseña.
       Solo se modifica la contraseña si viene explícitamente en el payload y con valor.
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'password' in data and data['password']:
            data['password'] = make_password(data['password'])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'password' in data:
            if data['password']:
                data['password'] = make_password(data['password'])
            else:
                data.pop('password', None)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserView(APIView):
    """
    Endpoint para que el usuario autenticado consulte sus propios datos personales.
    Requiere autenticación mediante Token JWT en el header: 'Authorization: Bearer <token>'
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
