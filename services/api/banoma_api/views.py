import os
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Profile, Video, Product, Purchase, Payment
from .serializers import (
    VideoSerializer, ProfileSerializer, ProductSerializer, PurchaseSerializer,
    PaymentSerializer, RegisterSerializer,
)
from . import payments as payment_service


def health(request):
    return JsonResponse({'status': 'ok'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class VideoUploadView(APIView):
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            from .tasks import transcode_video
            transcode_video.delay(video.id, video.file_url)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request, user_id):
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Profil non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProfileSerializer(profile).data)


class TalentListView(generics.ListAPIView):
    """Vitrine publique des talents, filtrable par compétence: /api/talents/?skill=python"""
    serializer_class = ProfileSerializer

    def get_queryset(self):
        qs = Profile.objects.all()
        skill = self.request.query_params.get('skill')
        if skill:
            qs = qs.filter(skills__icontains=skill)
        return qs


class ProductListCreateView(generics.ListCreateAPIView):
    """La marketplace du savoir : cours, ebooks, datasets, prestations, code source."""
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.all().order_by('-created_at')
        product_type = self.request.query_params.get('type')
        if product_type:
            qs = qs.filter(type=product_type)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class MyProductsView(generics.ListAPIView):
    """Boutique personnelle du créateur connecté."""
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')


class PurchaseCreateView(APIView):
    """Achat d'un article : calcule le split 70/30 puis initie le paiement (Stripe ou Mobile Money)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        provider = request.data.get('provider')  # 'stripe' | 'paypal' | 'mobile_money'
        phone = request.data.get('phone')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Produit introuvable'}, status=status.HTTP_404_NOT_FOUND)

        if product.seller_id == request.user.id:
            return Response({'error': "Vous ne pouvez pas acheter votre propre article"},
                             status=status.HTTP_403_FORBIDDEN)

        amount = product.price
        purchase = Purchase.objects.create(
            product=product, buyer=request.user, amount_paid=amount,
            platform_commission=round(amount * 0.30), creator_revenue=amount - round(amount * 0.30),
        )

        if provider == 'stripe':
            success_url = os.environ.get('PAYMENTS_SUCCESS_URL', 'http://localhost:3000/paiement/succes')
            cancel_url = os.environ.get('PAYMENTS_CANCEL_URL', 'http://localhost:3000/paiement/annule')
            session = payment_service.create_stripe_checkout_session(amount, product.currency, success_url, cancel_url)
            payment = Payment.objects.create(
                user=request.user, purchase=purchase, amount=amount, currency=product.currency,
                provider='stripe', reference=session.id,
            )
            return Response(
                {'purchase': PurchaseSerializer(purchase).data, 'checkout_url': session.url},
                status=status.HTTP_201_CREATED,
            )

        if provider == 'mobile_money':
            if not phone:
                purchase.delete()
                return Response({'error': 'phone requis pour mobile_money'}, status=status.HTTP_400_BAD_REQUEST)
            result = payment_service.charge_mobile_money(phone, amount)
            payment = Payment.objects.create(
                user=request.user, purchase=purchase, amount=amount, currency=product.currency,
                provider='mobile_money', reference=result.get('reference'),
            )
            return Response(
                {'purchase': PurchaseSerializer(purchase).data, 'mobile_money_status': result['status']},
                status=status.HTTP_201_CREATED,
            )

        purchase.delete()
        return Response({'error': 'provider doit être stripe ou mobile_money (paypal à venir)'},
                         status=status.HTTP_400_BAD_REQUEST)


class MyPurchasesView(generics.ListAPIView):
    """Historique d'achats de l'utilisateur connecté."""
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(buyer=self.request.user).order_by('-created_at')


class MySalesView(generics.ListAPIView):
    """Ventes réalisées par le créateur connecté, avec sa part de revenu (70 %)."""
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Purchase.objects.filter(product__seller=self.request.user).order_by('-created_at')


class PaymentWebhookMarkPaid(APIView):
    """Utilisé par le webhook Stripe pour confirmer un paiement."""
    def post(self, request):
        reference = request.data.get('reference')
        Payment.objects.filter(reference=reference).update(status='PAID')
        Purchase.objects.filter(payment__reference=reference).update(status='PAID')
        return Response({'ok': True})
