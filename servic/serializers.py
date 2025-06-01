from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ServiceProviderProfile, ProviderRequest

User = get_user_model() #Importamos el modelo de usuario desde el archivo models.py

#El serializador es el encargado de convertir los datos de la base de datos a un formato que pueda ser entendido por el cliente
#Si hacemos una comparacion con NodeJS, seria como el "userController.js"
#cual es la diferencia entre serializers y views.py? La diferencia es que el serializador es el encargado de convertir los datos de la base de datos a un formato que pueda ser entendido por el cliente
#y el views.py es el encargado de manejar las peticiones y respuestas de la API


# Serializador para registrar un usuario
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], error_messages={'required': 'La contraseña es obligatoria'})
    password2 = serializers.CharField(write_only=True, required=True, error_messages={'required': 'La contraseña no coincide'})
    first_name = serializers.CharField(required=True, error_messages={'required': 'El nombre es obligatorio'})
    last_name = serializers.CharField(required=True, error_messages={'required': 'El apellido es obligatorio'})
    email = serializers.EmailField(required=True, error_messages={'required': 'El email es obligatorio', 'invalid': 'El email no es valido', 'unique': 'El email ya esta registrado'})

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        #Generamos un username aleatorio
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email'].split('@')[0] 
        user = User.objects.create_user(**validated_data)
        return user 
    
    
    # Serializador para loguear un usuario 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Agrega datos del usuario a la respuesta
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'user_type': self.user.user_type,
        }
        return data   
    
    



#Serializador para mostrar y actualizar el perfil
#Aqui definimos los campos que queremos mostrar y actualizar en el perfil
#El email no se puede cambiar desde aquí
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type')
        read_only_fields = ('email', 'user_type')  # El email y user_type no se pueden cambiar desde aquí

#Serializador para el perfil de los prestadores de servicios
#Aqui definimos los campos que queremos mostrar y actualizar en el perfil
class ServiceProviderProfileSerializer(serializers.ModelSerializer):
    certification_file = serializers.FileField(
        required=True,
        error_messages={
            'required': 'El archivo de certificación es obligatorio',
            'invalid': 'El archivo de certificación no es válido'
        }
    )

    class Meta:
        model = ServiceProviderProfile
        fields = [
            'id', 'identification_type', 'identification_number', 
            'phone_number', 'address', 'city', 'state', 'country',
            'certification_file', 'certification_description', 
            'years_of_experience', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']

    def validate_certification_file(self, value):
        # Validar el tipo de archivo
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "El archivo debe ser una imagen (JPEG, PNG) o un PDF"
            )
        
        # Validar el tamaño del archivo (máximo 5MB)
        if value.size > 5 * 1024 * 1024:  # 5MB en bytes
            raise serializers.ValidationError(
                "El archivo no debe superar los 5MB"
            )
        return value

    def validate_identification_number(self, value):
        if ServiceProviderProfile.objects.filter(identification_number=value).exists():
            raise serializers.ValidationError("Este número de identificación ya está registrado")
        return value

    def validate_phone_number(self, value):
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("El número de teléfono debe contener solo dígitos, espacios, guiones y el símbolo +")
        return value

class UserRoleChangeSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        error_messages={
            'invalid_choice': 'El tipo de usuario debe ser "common" o "provider"'
        }
    )
    reason = serializers.CharField(
        required=True,
        max_length=500,
        error_messages={
            'required': 'Debe proporcionar una razón para el cambio de rol',
            'max_length': 'La razón no puede exceder los 500 caracteres'
        }
    )

    class Meta:
        model = User
        fields = ('user_type', 'reason')
        read_only_fields = ('id',)

    def validate(self, attrs):
        user = self.instance
        new_role = attrs['user_type']

        # Validar que no se intente cambiar al mismo rol
        if user.user_type == new_role:
            raise serializers.ValidationError(
                {"user_type": "El usuario ya tiene asignado este rol"}
            )

        # Validar que no se pueda cambiar el rol de un superusuario
        if user.is_superuser:
            raise serializers.ValidationError(
                {"user_type": "No se puede cambiar el rol de un superusuario"}
            )

        return attrs

class ProviderRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.SerializerMethodField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ProviderRequest
        fields = [
            'id', 'user_email', 'user_name', 'status', 'status_display',
            'request_reason', 'admin_response', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'admin_response', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

class ProviderRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRequest
        fields = ['request_reason']

    def validate(self, attrs):
        user = self.context['request'].user
        
        # Verificar que el usuario no sea ya un prestador
        if user.user_type == 'provider':
            raise serializers.ValidationError(
                "Ya eres un prestador de servicios"
            )
        
        # Verificar que no tenga una solicitud pendiente
        if ProviderRequest.objects.filter(
            user=user,
            status='pending'
        ).exists():
            raise serializers.ValidationError(
                "Ya tienes una solicitud pendiente"
            )
        
        return attrs

class ProviderRequestReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRequest
        fields = ['status', 'admin_response']

    def validate(self, attrs):
        if attrs['status'] == 'rejected' and not attrs.get('admin_response'):
            raise serializers.ValidationError(
                {"admin_response": "Debe proporcionar una razón para el rechazo"}
            )
        return attrs