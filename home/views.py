from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class studentAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print(request.user)
        student = Student.objects.all()
        student_serializer = StudentSerializer(student, many=True)
        return Response({
            'status' : 200,
            'payload' : student_serializer.data
        })
    
    
    def post(self, request):
        data = request.data
        post_serilizer = StudentSerializer(data = request.data)
        if not post_serilizer.is_valid():
            error=post_serilizer.errors
            return Response({
                "status" : 403,
                "errors" : error,
                "message" : "something went wrong"
            })
            
        post_serilizer.save()
        
        return Response({
            "status" : 200,
            "payload" : data,
            "message" : "data sent successfully"
        })
    
    def patch(self, request):
        try:
            student_obj = Student.objects.get(id=request.data['id'])
        except Student.DoesNotExist():
            return Response({
                'status' : 403,
                'message' : "Student doesnt exist"
            })
            
        student_serializer = StudentSerializer(student_obj, data=request.data, partial=True)
        
        if not student_serializer.is_valid():
            error=student_serializer.errors
            return Response({
                "status" : 403,
                "errors" : error,
                "message" : "something went wrong"
            })
            
        student_serializer.save()
        
        return Response({
            "status" : 200,
            "payload" : student_serializer.data,
            "message" : "data sent successfully"
        })
        
    def delete(self, request):
        try:
            id=request.data.get('id')
            student_obj = Student.objects.get(id=id)
            student_obj.delete()
            return Response({
                'status': 200,
                'message': 'Student deleted successfully'
            })
        except Exception as e:
                return Response({
                    'status': 403,
                    'message': 'Invalid id'
                })
            
        
class RegisterUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=request.data)
    
        if not serializer.is_valid():
            error = serializer.errors
            return Response({
                'status' : 403,
                'errors' : error,
                'message' : 'something went wrong'
            })
        
        serializer.save()
        
        user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)

        
        return Response({
            'status' : 200,
            'payload' : serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message' :'your data is saved'
        })   