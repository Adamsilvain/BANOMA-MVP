from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    """Badge de compétence attribué par pair review ou validation éditoriale BANOMA."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Profil scientifique certifiable d'un talent — dossier de compétences vivant."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=200, blank=True, help_text="Compétences séparées par des virgules")
    languages = models.CharField(max_length=200, blank=True)
    credibility_score = models.FloatField(
        default=0.0,
        help_text="Score de Crédibilité Scientifique (SCS) : calculé sur publications, citations, notes, interactions"
    )
    badges = models.ManyToManyField(Badge, blank=True, related_name='profiles')
    google_scholar_url = models.URLField(blank=True, help_text="Pour import futur des publications via DOI")

    def __str__(self):
        return f"Profil de {self.user.username}"


class Publication(models.Model):
    """Élément du parcours académique : diplôme, certification, publication ou projet."""
    TYPE_CHOICES = [
        ('DIPLOMA', 'Diplôme'),
        ('CERTIFICATION', 'Certification'),
        ('PUBLICATION', 'Publication scientifique'),
        ('PROJECT', 'Projet'),
    ]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='publications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    doi = models.CharField(max_length=100, blank=True, help_text="Digital Object Identifier, si applicable")
    year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_display()} — {self.title}"


class Video(models.Model):
    """Contenu vidéo éducatif (portfolio, cours, extrait de conférence)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    """Article de la boutique personnelle d'un créateur — la marketplace du savoir."""
    TYPE_CHOICES = [
        ('COURS', 'Cours'),
        ('EBOOK', 'Ebook'),
        ('DATASET', 'Dataset'),
        ('CARTE', 'Carte / ressource cartographique'),
        ('PRESTATION', 'Prestation de conseil'),
        ('CODE_SOURCE', 'Code source'),
    ]
    REVENUE_MODEL_CHOICES = [
        ('ONE_TIME', 'Paiement unique'),
        ('SUBSCRIPTION', 'Abonnement mensuel'),
        ('DONATION', 'Don libre'),
        ('PER_CHAPTER', 'Accès par chapitre'),
    ]
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='COURS')
    revenue_model = models.CharField(max_length=20, choices=REVENUE_MODEL_CHOICES, default='ONE_TIME')
    price = models.PositiveIntegerField(default=0, help_text="Prix en centimes (0 si don libre)")
    currency = models.CharField(max_length=10, default='XOF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Règle d'or BANOMA : 70 % des revenus reviennent au créateur, 30 % à la plateforme.
PLATFORM_COMMISSION_RATE = 0.30


class Purchase(models.Model):
    """Achat d'un article de la marketplace, avec split de revenus 70/30 créateur/plateforme."""
    STATUS_CHOICES = [
        ('PENDING', 'En attente de paiement'),
        ('PAID', 'Payé'),
        ('FAILED', 'Échoué'),
        ('REFUNDED', 'Remboursé'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    amount_paid = models.PositiveIntegerField(help_text='Montant total payé, en centimes')
    platform_commission = models.PositiveIntegerField(help_text='Part BANOMA (30 %), en centimes')
    creator_revenue = models.PositiveIntegerField(help_text='Part créateur (70 %), en centimes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcule automatiquement le split 70/30 à partir du montant payé.
        if not self.pk or self.platform_commission is None:
            self.platform_commission = round(self.amount_paid * PLATFORM_COMMISSION_RATE)
            self.creator_revenue = self.amount_paid - self.platform_commission
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer.username} -> {self.product.title} ({self.status})"


class Payment(models.Model):
    """Transaction de paiement (Stripe, PayPal ou Mobile Money via CinetPay), liée à un achat."""
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('mobile_money', 'Mobile Money (Wave / Orange Money / Moov)'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
        ('FAILED', 'Échoué'),
        ('REFUNDED', 'Remboursé'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, null=True, blank=True, related_name='payment')
    amount = models.PositiveIntegerField(help_text='Montant en centimes')
    currency = models.CharField(max_length=10, default='XOF')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount/100} {self.currency} ({self.provider}) - {self.status}"
