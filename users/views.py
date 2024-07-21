from datetime import datetime

import pytz
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView

from config import settings
from users.permissions import IsOwner, IsModerator
from users.models import Payment, User
from users.serializer import (
    PaymentSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
)


# Create your views here.
class PaymentCreateAPIView(CreateAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class PaymentListAPIView(ListAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["pay_day"]
    filterset_fields = ["paid_course", "payment_method"]
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(RetrieveAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentUpdateAPIView(UpdateAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentDestroyAPIView(DestroyAPIView):

    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_actine=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsOwner | IsModerator,
    )


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsOwner | IsModerator,
    )

    @staticmethod
    def verification_view(token):
        user = User.objects.filter(verification_code=token).first()
        if user:
            user.is_active = True
            user.save()
        return redirect("users:login")


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def perform_authentication(self, request):
        user = User.objects.filter(verification_code=self.request.token).first()
        if user:
            zone = pytz.timezone(settings.TIME_ZONE)
            user.last_login = datetime.now(zone)
            user.save()
