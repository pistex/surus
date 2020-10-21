from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.conf import settings
from django.contrib import auth
User = auth.get_user_model()


class MyAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        context['activate_url'] = settings.FRONTEND_URL + \
            'confirm_email/' + context['key']
        msg = self.render_mail(template_prefix, email, context)
        msg.send()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            user = User.objects.get(email=user.email)
            sociallogin.state['process'] = 'connect'
            perform_login(request, user, 'none')
        except User.DoesNotExist:
            pass
