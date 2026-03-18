from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from core.serializers import CreateAPIKeySerializer
from core.services import KeyGenerator
from core.exceptions import KeyGenerationError
from core.models import KeyInformation
from core.utils import get_user_role

from datetime import datetime as dt, timezone







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



class DeleteAPIKeyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        key = get_object_or_404(KeyInformation, key_id=pk)

        if request.user.role != 1:  # not superadmin 
            if key.company_id != request.user.company_id:
                 return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
        key.key_status = 2
        key.save()
        return Response({"message":"key deleted successfully"}, status=status.HTTP_200_OK)
    

class GetUserDetailsFromTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] # If user was not authenticated i wouldnt have recieved this inside the view

    def get(self, request):
        data = {}
        user = request.user
        try:
            data["user_id"] = user.user_id
            data["username"] = user.username
            data["role"] = get_user_role(user.role) # provide role in string rather than ineteger id
        except Exception as e:
            return Response({"Error": f"Error occured while fetching details from request.user:{e}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exp_epoch = request.auth.payload["exp"]
            expiry = dt.fromtimestamp(exp_epoch, tz=timezone.utc) # considering UTC timezone only
           
        except Exception as e:
            return Response({"error":f"Error occured while accessing expiry time {e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            data["token_expiry_time"] = expiry
        return Response(data, status=status.HTTP_200_OK)

    


