from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Residence

class ResidenceSerializer(ModelSerializer):
    class Meta:
        fields = ["identifier","owner","created_by","created_at","updated_at"]
        model = Residence
        # read_only_fields = ["identifier", "created_by", "created_at", "updated_at"]

    def validate_owner(self,user):
        if user.is_superuser:
            raise ValidationError("Un usuario administrador no puede ser dueño de una residencia")
        return user

    def validate_identifier(self,value):
        identifier = value.upper()
        
        if Residence.objects.filter(identifier=identifier).exists():
            raise ValidationError("Ya existe una residencia registrada con ese identificador")
        
        return identifier
    

class UpdateResidenceSerializer(ModelSerializer):
    class Meta:
        model = Residence
        fields = ["identifier", "owner", "created_by", "created_at", "updated_at"]
        read_only_fields = ["identifier", "created_by", "created_at", "updated_at"]

    def validate_owner(self, user):
        if user.is_superuser:
            raise ValidationError("Un usuario administrador no puede ser dueño de una residencia")
        return user