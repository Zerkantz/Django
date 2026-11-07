import zeep
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import RegisterUserSerializer, UserSerializer


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
    Web Service Propio:
    Endpoint para que el usuario autenticado consulte sus propios datos personales.
    Requiere autenticación mediante Token JWT en el header: 'Authorization: Bearer <token>'
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterUserView(APIView):
    """
    Endpoint público para el registro de nuevos usuarios en la plataforma.
    No requiere autenticación previa.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'telefono': user.telefono,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoapCountryView(APIView):
    """
    Consumo SOAP (Unidad 3):
    Endpoint que consume el servicio web SOAP público CountryInfoService mediante la librería Zeep.
    Retorna información de país (nombre, capital, moneda, código telefónico) dado su código ISO.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.query_params.get('code', 'MX').upper().strip()
        wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
        try:
            client = zeep.Client(wsdl=wsdl)
            name = client.service.CountryName(sCountryISOCode=code)
            capital = client.service.CapitalCity(sCountryISOCode=code)
            currency = client.service.CountryCurrency(sCountryISOCode=code)
            phone_code = client.service.CountryIntPhoneCode(sCountryISOCode=code)

            return Response({
                'status': 'success',
                'protocol': 'SOAP (WSDL)',
                'client_library': 'zeep',
                'service_url': wsdl,
                'country_code': code,
                'country_name': name,
                'capital': capital,
                'currency': {
                    'name': getattr(currency, 'sName', 'Pesos'),
                    'iso_code': getattr(currency, 'sISOCode', 'MXN'),
                },
                'phone_code': phone_code,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'protocol': 'SOAP (WSDL)',
                'message': f'Error al consumir el servicio SOAP: {str(e)}',
                'country_code': code,
            }, status=status.HTTP_502_BAD_GATEWAY)
