import random
import string
import time

from django.contrib.auth import get_user_model, login
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, UpdateView
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ClientUser
from .forms import NumberForm, CheckNumberForm, ProfileForm
from .serializers import NumberSerializer, CheckNumberSerializer, ClientSerializer


def generate_code(length):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=length))
    return code

User = get_user_model()

class HomePageView(TemplateView):
    template_name = 'refsys/index.html'


class NumberFormPageView(FormView):
    template_name = 'refsys/number_form.html'
    form_class = NumberForm
    success_url = reverse_lazy('check_code_form')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            number = form.cleaned_data['number']
            code = generate_code(4)
            cache.set("number", number, timeout=300)
            cache.set(f'auth_code_{number}', code, timeout=300)
            time.sleep(2)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CheckCodeFormPageView(FormView):
    template_name = 'refsys/check_code_form.html'
    form_class = CheckNumberForm
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        number = cache.get('number')
        cached_code = cache.get(f'auth_code_{number}')
        form = CheckNumberForm(initial={'number': number, 'code': cached_code})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            number = form.cleaned_data['number']
            code = form.cleaned_data['code']
            cached_code = cache.get(f'auth_code_{number}')
            if cached_code != code:
                form.add_error('code', "неверный код")
                return self.form_invalid(form)
            else:
                client, created = User.objects.get_or_create(username=number,
                                                             defaults={'invite_code': generate_code(6)})
                if created:
                    client.set_password(generate_code(8))
                    client.save()
                token, _ = Token.objects.get_or_create(user=client)
                login(request, client)
                cache.delete(f'auth_code_{number}')
                cache.delete('number')
                return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ProfileView(UpdateView):
    template_name = 'refsys/profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_invite = context['clientuser'].invite_code
        referals = ClientUser.objects.filter(other_code=my_invite)
        context['referals'] = referals
        return context


class APIRequestCode(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = NumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            code = generate_code(4)
            cache.set(f'auth_code_{number}', code, timeout=120)
            time.sleep(2)
            return Response({'detail': f'Отправлен код {code} на номер {number}'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APICheckCode(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = CheckNumberSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            number = serializer.validated_data['number']
            code = serializer.validated_data['code']

            cached_code = cache.get(f'auth_code_{number}')
            if cached_code != code:
                return Response({"detail": "Неверный код."}, status=status.HTTP_400_BAD_REQUEST)


            client, created = User.objects.get_or_create(username=number,
                                                         defaults={'invite_code': generate_code(6)})
            if created:
                client.set_password(generate_code(8))
                client.save()
            token, _ = Token.objects.get_or_create(user=client)
            cache.delete(f'auth_code_{number}')
            return Response({"token": f"{token.key}"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

