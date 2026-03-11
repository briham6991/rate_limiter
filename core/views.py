from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.serializers import CreateAPIKeySerializer
from core.services import KeyGenerator
from core.exceptions import KeyGenerationError



class CreateAPIKeyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy() # Cause i dont want to change the data inside the request data which has to remain immutable
        try:
            key = KeyGenerator()
            actual_key, hashed_key = key.get_keys()
        except KeyGenerationError as e:
            return Response(f'{e.__repr__()}', status = status.HTTP_417_EXPECTATION_FAILED)
        except Exception as e:
            return Response(f'{e.__repr__()}', status = status.HTTP_400_BAD_REQUEST)
        
        data["key_value"] = hashed_key
        data["created_by"] = request.user.user_id
        
        serializer = CreateAPIKeySerializer(data=data) # Modified earlier only used data inside
        if serializer.is_valid():
            serializer.save()
            return Response({"actual_key":actual_key, "details":serializer.data}, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
