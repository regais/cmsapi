from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import ContentModel

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    DjangoModelPermissions,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny,
)
from .serializers import (
     PostCreateUpdateSerializer,
     PostDetailSerializer,
     SearchSerializer,
     UserSerializer, 
     ProfileSerializer
)
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.generics import ListAPIView

from rest_framework import generics, permissions
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    #permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
        "user": ProfileSerializer(profile, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(profile.user)[1]
        })



class UserWritePermission(BasePermission):
    
    message = "Only Author or Admin has edit/delete permission." 
    def has_object_permission(self,request,view,obj):
        
        #Check if method is safe
        if request.method in SAFE_METHODS:
            return True
        
        #Check if requesting user is author or is admin
        return (obj.author == request.user) or (request.user.is_superuser)
        

class CreatePostAPIView(generics.GenericAPIView):
    serializer_class = PostCreateUpdateSerializer
    queryset = ContentModel.objects.all()   
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        #Default queryset
        queryset = ContentModel.objects.filter(author=self.request.user) # Show current user's posts
        
        #Show all posts if admin
        if self.request.user.is_superuser:
            queryset = ContentModel.objects.all()  
            
        serializer = self.get_serializer(queryset,many=True)

        return Response(serializer.data)
        
    def post(self, request,*args,**kwargs):
        data=request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            #Save post and set the author as current requesting user
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

            

    
class FetchUpdateDeleteView(APIView,UserWritePermission):
    permission_classes = [UserWritePermission]
    def get_object(self, pk):
        # Returns an object instance that should 
        # be used for detail views.
        try:
            return ContentModel.objects.get(pk=pk)
        except ContentModel.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        content = self.get_object(pk)
        serializer_class = PostDetailSerializer(content)
        permission_classes = [UserWritePermission]
        return Response(serializer_class.data)
  
    def put(self, request, pk, format=None):
        contnet = self.get_object(pk)
        serializer = PostDetailSerializer(content, data=request.data)
        permission_classes = [UserWritePermission]
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
    def patch(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = PostDetailSerializer(queryset,
                                           data=request.data,
                                           partial=True)
        permission_classes = [UserWritePermission]
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
  
    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        permission_classes = [UserWritePermission]
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)      
    
    def get_queryset(self):
        user = self.request.user
        return ContentModel.objects.filter(author=user)
    
    
class SearchFilterAPIView(ListAPIView):  
    serializer_class = SearchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter,OrderingFilter)
    search_fields = ('title','body','summary','categories')
    
    def get_queryset(self):
        queryset = ContentModel.objects.filter(author=self.request.user) # Show current user's posts
        
        #Show all posts if admin
        if self.request.user.is_superuser:
            queryset = ContentModel.objects.all()  
        return queryset