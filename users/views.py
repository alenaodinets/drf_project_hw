from rest_framework import viewsets, filters
from users.models import Payment
from users.serializer import PaymentSerializer
# Create your views here.


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [filters.OrderingFilter]
    filterset_fields = ['paid_course', 'payment_method']
    ordering_fields = ('pay_day',)
