from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Vitrine d'un talent scientifique/technique."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=200, blank=True, help_text="Compétences séparées par des virgules")
    languages = models.CharField(max_length=200, blank=True)
    credibility_score = models.FloatField(default=0.0)

    def __str__(self):
        return f"Profil de {self.user.username}"


class Video(models.Model):
    """Contenu de portfolio (démo, pitch) soumis par un talent."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Opportunity(models.Model):
    """Offre de mission/emploi/collaboration publiée par un recruteur."""
    TYPE_CHOICES = [
        ('MISSION', 'Mission'),
        ('EMPLOI', 'Emploi'),
        ('COLLABORATION', 'Collaboration'),
        ('FORMATION', 'Formation'),
    ]
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='MISSION')
    location = models.CharField(max_length=200, blank=True)
    remote = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    """Candidature d'un talent à une opportunité."""
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('ACCEPTED', 'Acceptée'),
        ('REJECTED', 'Refusée'),
        ('WITHDRAWN', 'Retirée'),
    ]
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('opportunity', 'applicant')

    def __str__(self):
        return f"{self.applicant.username} -> {self.opportunity.title}"


class Payment(models.Model):
    """Paiement lié à une prestation (Stripe ou Mobile Money)."""
    PROVIDER_CHOICES = [('stripe', 'Stripe'), ('mobile_money', 'Mobile Money')]
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
        ('FAILED', 'Échoué'),
        ('REFUNDED', 'Remboursé'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.PositiveIntegerField(help_text='Montant en centimes')
    currency = models.CharField(max_length=10, default='XOF')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount/100} {self.currency} ({self.provider}) - {self.status}"
