from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    VideoUploadView, ProfileView, TalentListView, OpportunityListCreateView, health,
    RegisterView, ApplicationCreateView, MyApplicationsView,
    PaymentCreateView, MyPaymentsView,
)

urlpatterns = [
    path('health/', health, name='health'),

    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Talents / profils
    path('profiles/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('talents/', TalentListView.as_view(), name='talent-list'),

    # Opportunités / candidatures
    path('opportunities/', OpportunityListCreateView.as_view(), name='opportunity-list'),
    path('applications/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/mine/', MyApplicationsView.as_view(), name='application-mine'),

    # Vidéos / portfolio
    path('videos/', VideoUploadView.as_view(), name='video-upload'),

    # Paiements
    path('payments/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/mine/', MyPaymentsView.as_view(), name='payment-mine'),
]
