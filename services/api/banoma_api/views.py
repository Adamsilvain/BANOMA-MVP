import os
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Profile, Video, Opportunity
from .serializers import VideoSerializer, ProfileSerializer, OpportunitySerializer


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


class OpportunityListCreateView(generics.ListCreateAPIView):
    queryset = Opportunity.objects.all().order_by('-created_at')
    serializer_class = OpportunitySerializer


def health(request):
    return JsonResponse({'status': 'ok'})


from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Application, Payment
from .serializers import ApplicationSerializer, PaymentSerializer, RegisterSerializer
from . import payments as payment_service


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)


class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).order_by('-created_at')


class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'XOF')
        provider = request.data.get('provider')  # 'stripe' | 'mobile_money'
        phone = request.data.get('phone')

        if not amount or provider not in ('stripe', 'mobile_money'):
            return Response({'error': 'amount et provider (stripe|mobile_money) requis'},
                             status=status.HTTP_400_BAD_REQUEST)

        if provider == 'stripe':
            success_url = os.environ.get('PAYMENTS_SUCCESS_URL', 'http://localhost:3000/paiement/succes')
            cancel_url = os.environ.get('PAYMENTS_CANCEL_URL', 'http://localhost:3000/paiement/annule')
            session = payment_service.create_stripe_checkout_session(amount, currency, success_url, cancel_url)
            payment = Payment.objects.create(
                user=request.user, amount=amount, currency=currency, provider='stripe', reference=session.id
            )
            return Response({'payment': PaymentSerializer(payment).data, 'checkout_url': session.url},
                             status=status.HTTP_201_CREATED)

        if not phone:
            return Response({'error': 'phone requis pour mobile_money'}, status=status.HTTP_400_BAD_REQUEST)
        result = payment_service.charge_mobile_money(phone, amount)
        payment = Payment.objects.create(
            user=request.user, amount=amount, currency=currency, provider='mobile_money',
            reference=result.get('reference')
        )
        return Response({'payment': PaymentSerializer(payment).data, 'mobile_money_status': result['status']},
                         status=status.HTTP_201_CREATED)


class MyPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')
