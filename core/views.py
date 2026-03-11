from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import KeyInformation
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.serializers import CreateAPIKeySerializer
from core.services import KeyGenerator
from core.exceptions import KeyGenerationError


class CreateAPIKeyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            key = KeyGenerator()
            actual_key, hashed_key = key.get_keys()
        except KeyGenerationError as e:
            return Response(f'{e.__repr__()}', status = status.HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            return Response(f'{e.__repr__()}', status = status.HTTP_400_BAD_REQUEST)
        
        data["key_value"] = hashed_key
        data["created_by"] = request.user.user.id
        
        serializer = CreateAPIKeySerializer(data=data) # Modified earlier only used data inside
        if serializer.is_valid():
            serializer.save()
            return Response({"actual_key":actual_key, "details":serializer.data}, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

        
         # This is actual key

        


        # Extract company_id, plan_id, activation_time, valid_till from request.data
        # Generate a SHA-256 API key internally
        # Store the hashed key in database
        # Return the plain text key once in the response
        

# Takes company_id, plan_id, activation_time, valid_till as input
# Generates a SHA-256 API key internally
# Stores the hashed key in database
# Returns the plain text key once in the response









# Create your views here.
