from .models import Invitation
from rest_framework.serializers import ModelSerializer


class InvitationSerializer(ModelSerializer):
    class Meta:
        model = Invitation
        fields = "__all__"
        read_only_fields=["id","code","host","created_at"]
