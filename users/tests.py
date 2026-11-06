from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from users.serializers import UserSerializer

User = get_user_model()


class UserModelTestCase(TestCase):
    def test_create_user_with_email_and_telefono(self):
        user = User.objects.create_user(
            email='cliente@tienda.local',
            password='Password123!',
            telefono='555-123-4567',
            first_name='Carlos',
            last_name='Gómez'
        )
        self.assertEqual(user.email, 'cliente@tienda.local')
        self.assertEqual(user.telefono, '555-123-4567')
        self.assertTrue(user.check_password('Password123!'))
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@tienda.local',
            password='AdminPassword123!'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SecurityFixesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@tienda.local',
            password='AdminSecretPassword123!'
        )
        self.regular_user = User.objects.create_user(
            email='usuario@tienda.local',
            password='UserOriginalPassword123!',
            telefono='555-987-6543',
            first_name='Ana',
            last_name='López'
        )

    def test_security_fix_1_password_not_exposed_in_serializer(self):
        """
        Falla de seguridad 1 corregida:
        El hash de la contraseña nunca debe aparecer en la respuesta serializada.
        """
        serializer = UserSerializer(self.regular_user)
        self.assertNotIn('password', serializer.data)
        self.assertEqual(serializer.data['email'], 'usuario@tienda.local')
        self.assertEqual(serializer.data['telefono'], '555-987-6543')

    def test_security_fix_1_password_not_exposed_in_auth_me(self):
        """
        La contraseña nunca debe figurar en el endpoint /api/v1/auth/me/
        """
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)
        self.assertEqual(response.data['email'], 'usuario@tienda.local')
        self.assertEqual(response.data['telefono'], '555-987-6543')

    def test_security_fix_2_partial_update_without_password_does_not_change_password(self):
        """
        Falla de seguridad 2 corregida:
        Al actualizar un usuario sin enviar contraseña, el manual asignaba la contraseña
        del usuario que hacía la petición (request.user.password).
        Aquí comprobamos que:
        1. La contraseña del usuario NO cambia.
        2. La contraseña del usuario NO se convierte en la del administrador.
        3. El usuario aún puede autenticarse con su contraseña original.
        """
        self.client.force_authenticate(user=self.admin_user)
        original_hash = self.regular_user.password

        # El admin actualiza solo el teléfono y el nombre de regular_user (sin enviar contraseña)
        response = self.client.patch(
            f'/api/v1/users/{self.regular_user.id}/',
            {'telefono': '555-000-1111', 'first_name': 'Ana María'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        # Refrescamos desde la BD
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.telefono, '555-000-1111')
        self.assertEqual(self.regular_user.first_name, 'Ana María')

        # Verificación crítica de seguridad:
        self.assertEqual(self.regular_user.password, original_hash)
        self.assertTrue(self.regular_user.check_password('UserOriginalPassword123!'))
        self.assertFalse(self.regular_user.check_password('AdminSecretPassword123!'))

    def test_partial_update_with_new_password_changes_password_correctly(self):
        """
        Cuando sí se envía una nueva contraseña, debe actualizarse correctamente y encriptarse.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(
            f'/api/v1/users/{self.regular_user.id}/',
            {'password': 'NewBrandPassword456!'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('password', response.data)

        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('NewBrandPassword456!'))
        self.assertFalse(self.regular_user.check_password('UserOriginalPassword123!'))


class JWTAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='jwt_user@tienda.local',
            password='MyJwtPassword123!',
            telefono='555-444-3333'
        )

    def test_obtain_token_with_email(self):
        """
        Verifica que el login con JWT utiliza 'email' como identificador.
        """
        response = self.client.post('/api/v1/auth/token/', {
            'email': 'jwt_user@tienda.local',
            'password': 'MyJwtPassword123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Verificar tiempo de expiración del token configurado (2 horas)
        token = AccessToken(response.data['access'])
        exp_seconds = token['exp'] - token['iat']
        self.assertAlmostEqual(exp_seconds, 7200, delta=60)

    def test_auth_me_with_jwt_token(self):
        """
        Verifica el acceso a /api/v1/auth/me/ usando el token JWT en el Header.
        """
        token_resp = self.client.post('/api/v1/auth/token/', {
            'email': 'jwt_user@tienda.local',
            'password': 'MyJwtPassword123!'
        })
        access_token = token_resp.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/v1/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'jwt_user@tienda.local')
        self.assertEqual(response.data['telefono'], '555-444-3333')
        self.assertNotIn('password', response.data)
