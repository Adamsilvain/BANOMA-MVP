from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    health, RegisterView,
    VideoUploadView, ProfileView, TalentListView,
    ProductListCreateView, MyProductsView,
    PurchaseCreateView, MyPurchasesView, MySalesView,
    PaymentWebhookMarkPaid,
)

urlpatterns = [
    path('health/', health, name='health'),

    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Talents / profils scientifiques
    path('profiles/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('talents/', TalentListView.as_view(), name='talent-list'),

    # Marketplace du savoir (cours, ebooks, datasets, prestations, code source)
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/mine/', MyProductsView.as_view(), name='product-mine'),
    path('purchases/', PurchaseCreateView.as_view(), name='purchase-create'),
    path('purchases/mine/', MyPurchasesView.as_view(), name='purchase-mine'),
    path('sales/mine/', MySalesView.as_view(), name='sales-mine'),

    # Vidéos éducatives
    path('videos/', VideoUploadView.as_view(), name='video-upload'),

    # Webhook paiement
    path('payments/webhook/mark-paid/', PaymentWebhookMarkPaid.as_view(), name='payment-webhook'),
]
