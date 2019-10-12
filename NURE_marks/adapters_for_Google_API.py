# from allauth.socialaccount.adaptor import DefaultSocialAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import render_to_response

class MySocialAccount(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        u = sociallogin.user
        # Потом раскоментить!!!!
    #     if not u.email.split('@')[1] == "nure.ua":
    #         raise ImmediateHttpResponse(render_to_response('Login/error.html'))