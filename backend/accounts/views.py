from django.http import HttpResponse
from django.views.generic import TemplateView

class EmailVerificationView(TemplateView):
    template_name = 'account/registration/register.html'
    def get(self, request, uidb64, token):
        # For testing purposes, just return a basic response
        return HttpResponse("Email verified!")
