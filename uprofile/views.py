from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from uprofile.serializers import *

from btcsandbox.utils import search_list, set_username


class UpdateView(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]
    
    def put(self, request, format=None):
        obj = request.user
        response_data = {}
        serializer = UpdateProfileSerializer(obj, data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            
            if username == obj.username:
                serializer.save()
                
                response_data['status'] = status.HTTP_200_OK
                response_data['success'] = True
                response_data['result'] = "Profile has been updated."
                
                return Response(data=response_data, status=response_data['status'])
            
            else:
                if search_list(username, [i.username for i in Account.objects.all()]):
                    response_data['status'] = status.HTTP_226_IM_USED
                    response_data['success'] = False
                    response_data['result'] = "Username is in use."
                    
                    return Response(data=response_data, status=response_data['status'])
                
                else:
                    set_username(username, obj)
                    serializer.save()
                
                    response_data['status'] = status.HTTP_200_OK
                    response_data['success'] = True
                    response_data['result'] = "Profile has been updated."
                    
                    return Response(data=response_data, status=response_data['status'])
        
        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


# Update Email
class UpdateEmail(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]
    
    def put(self, request, format=None):
        obj = request.user
        response_data = {}
        serializer = UpdateEmail(data=request.data)
        
        if serializers.is_valid():
            pass
        
        
        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])