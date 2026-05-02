from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import IsOwnerOrSelf, IsAdminOnly
from .authentication import JWTOrAPITokenAuthentication


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


class UsuarioRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrSelf]

    def get_queryset(self):
        return Usuario.objects.filter(id=self.request.user.id)


class UsuarioMeView(APIView):
    authentication_classes = [JWTOrAPITokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class AuthLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        senha = request.data.get('senha')

        if not email or not senha:
            return Response({'detail': 'E-mail e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'detail': 'E-mail ou senha inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(senha):
            return Response({'detail': 'E-mail ou senha inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        serializer = UsuarioSerializer(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': serializer.data,
        })


class AuthRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = UsuarioSerializer(user).data
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'usuario': response_data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
