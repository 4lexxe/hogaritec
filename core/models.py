import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

Customer = get_user_model()

class PasswordReset(models.Model):
    email = models.EmailField()  # Puede que lo necesites si deseas almacenar el correo directamente
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='password_resets')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Si no hay fecha de expiración configurada, se establece a 1 hora desde la creación
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=3)
        super().save(*args, **kwargs)

    def is_valid(self):
        # Verifica si el token aún es válido
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"Password reset token for {self.user.email} - Expires at {self.expires_at}"

    class Meta:
        indexes = [
            models.Index(fields=['expires_at']),
            models.Index(fields=['user']),
        ]