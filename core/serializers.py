from rest_framework.serializers import ModelSerializer
from core.models import KeyInformation

class CreateAPIKeySerializer(ModelSerializer):

    class Meta:
        model = KeyInformation
        fields = ["key_id", "key_status", "key_value", "company_id", "plan_id", "activation_time", "valid_till","created_by"]
        
        read_only_fields = ["key_id"] # Not included KeyStatus in here cause this can be changed while iam writing it
        extra_kwargs = {"key_value": {"write_only": True}} # this ensures that hashed key is not exposed in any API response, it can only be used for writing to database
            