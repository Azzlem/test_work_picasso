from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from users.serializers import  UserCreateSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    @swagger_auto_schema(operation_summary="Создание пользователя")
    def post(self, request, *args, **kwargs):
        return super(UserCreateView, self).post(request, *args, **kwargs)

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_user.set_password(self.request.data["password"])
        new_user.save()
