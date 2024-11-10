from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        return render(request, 'users/login.html', {'error': 'Invalid credentials'})
