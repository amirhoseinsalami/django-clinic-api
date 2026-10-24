from django.urls import path
from .views import PaymentCallbackView, CreatePaymentView

urlpatterns = [
    path('create/', CreatePaymentView.as_view()),
    path('callback/', PaymentCallbackView.as_view())
]