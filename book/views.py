from django.shortcuts import render

# Create your views here.
from .serializers import BookSerializer,BookModelSerializers,LoginSerializers
from .models import Book
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions

@csrf_exempt
def book_list(request):
    if request.method=="GET":
        books=Book.objects.all()
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)
    elif request.method=="POST":
        data=JSONParser().parse(request)
        serializer=BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        else:
            return JsonResponse(serializer.errors,status=400)

@csrf_exempt
def book_detail(request,id):
    if request.method=="GET":
        book=Book.objects.get(id=id)
        serializer=BookSerializer(book)
        return JsonResponse(serializer.data)
    elif request.method=="PUT":
        book = Book.objects.get(id=id)
        data=JSONParser().parse(request)
        serializer=BookSerializer(book,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
    elif request.method=="DELETE":
        book = Book.objects.get(id=id)
        book.delete()
        return HttpResponse(status=204)

class BookList(APIView):
    def get(self,request):
        books=Book.objects.all()
        serializer=BookModelSerializers(books,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=BookModelSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    def getobj(self,id):
        return Book.objects.get(id=id)
    def get(self,request,id):
        book=self.getobj(id)
        seializer=BookModelSerializers(book)
        return Response(seializer.data)
    def put(self,request,id):
        book=self.getobj(id)
        serializer=BookModelSerializers(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        book=self.getobj(id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BooksListMixin(mixins.ListModelMixin,generics.GenericAPIView,mixins.CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers
    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

class BookDetailMixin(generics.GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin
                    ,mixins.DestroyModelMixin):

    authentication_classes = [TokenAuthentication,]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookModelSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy( request, *args, **kwargs)

class LoginApi(APIView):

    def post(self,request):
        serializer=LoginSerializers(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                token,created=Token.objects.get_or_create(user=user)
                return Response({"token":token.key},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)
                # return Response("error occured", status=400)

class LogoutApi(APIView):
    def get(self,request):
        logout(request)
        request.user.auth_token.delete()


