from allauth.socialaccount.models import SocialAccount
def social_account_check(user, provider):
    return SocialAccount.objects.filter(user=user, provider=provider).exists()
