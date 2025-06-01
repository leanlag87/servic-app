from django.contrib.auth.models import AbstractUser
from django.db import models

# Aqui definimos los modelos de la base de datos como hacemos en NodeJS

# Modelo de tabla para almacenar usuarios
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('common', 'Usuario Común'),
        ('provider', 'Prestador de Servicios'),
    )
    
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    is_profile_complete = models.BooleanField(default=False)
    
    # Usar email como campo de autenticación
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


#Modelo para el perfil de los prestadores de servicios
class ServiceProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    identification_type = models.CharField(max_length=20, choices=[
        ('dni', 'DNI'),
        ('ce', 'Carné de Extranjería'),
        ('passport', 'Pasaporte')
    ])
    identification_number = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    certification_file = models.FileField(upload_to='certifications/')
    certification_description = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Perfil de {self.user.email}"

    class Meta:
        verbose_name = "Perfil de Prestador"
        verbose_name_plural = "Perfiles de Prestadores"

class UserRoleChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='role_changes')
    previous_role = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES)
    new_role = models.CharField(max_length=10, choices=User.USER_TYPE_CHOICES)
    reason = models.TextField()
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='role_changes_made')
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de cambio de rol"
        verbose_name_plural = "Registros de cambios de rol"
        ordering = ['-changed_at']

    def __str__(self):
        return f"Cambio de rol de {self.user.email} de {self.previous_role} a {self.new_role}"

class ProviderRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobada'),
        ('rejected', 'Rechazada')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='provider_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_reason = models.TextField(help_text="Razón por la que desea convertirse en prestador")
    admin_response = models.TextField(blank=True, null=True, help_text="Respuesta del administrador")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='reviewed_requests'
    )

    class Meta:
        verbose_name = "Solicitud de Prestador"
        verbose_name_plural = "Solicitudes de Prestadores"
        ordering = ['-created_at']

    def __str__(self):
        return f"Solicitud de {self.user.email} - {self.get_status_display()}"