import logging
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import IsOwnerOrSelf, IsAdminOnly
from .authentication import JWTOrAPITokenAuthentication

logger = logging.getLogger(__name__)


class UsuarioCreatedListView(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        if self.request.method == 'POST':
            return [IsAdminOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_authenticated', False):
            if getattr(user, 'is_staff', False):
                return Usuario.objects.all()
            return Usuario.objects.filter(id=user.id)
        return Usuario.objects.none()

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f'Novo usuário criado: {serializer.instance.email}')


class UsuarioRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrSelf]

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f'Usuário atualizado: {serializer.instance.email}')

    def perform_destroy(self, instance):
        email = instance.email
        instance.delete()
        logger.warning(f'Usuário deletado: {email}')


class UsuarioMeView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UsuarioSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f'Erro ao buscar usuário logado: {str(e)}')
            return Response(
                {'detail': 'Erro ao buscar informações do usuário.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email', '').lower().strip()
        senha = request.data.get('senha', '')

        if not email or not senha:
            logger.warning(f'Tentativa de login sem credenciais')
            return Response(
                {'detail': 'E-mail e senha são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            logger.warning(f'Tentativa de login com email inválido: {email}')
            return Response(
                {'detail': 'E-mail ou senha inválidos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(senha):
            logger.warning(f'Tentativa de login com senha incorreta: {email}')
            return Response(
                {'detail': 'E-mail ou senha inválidos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken.for_user(user)
            serializer = UsuarioSerializer(user)
            logger.info(f'Login bem-sucedido: {email}')
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'usuario': serializer.data,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Erro ao gerar tokens para {email}: {str(e)}')
            return Response(
                {'detail': 'Erro ao processar login.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AuthRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                response_data = UsuarioSerializer(user).data
                logger.info(f'Novo usuário registrado: {user.email}')
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'usuario': response_data,
                }, status=status.HTTP_201_CREATED)
            
            logger.warning(f'Erro no registro: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Erro inesperado no registro: {str(e)}')
            return Response(
                {'detail': 'Erro ao registrar usuário.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

