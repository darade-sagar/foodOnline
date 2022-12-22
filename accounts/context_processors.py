from vendor.models import Vendor
from .models import UserProfile

def get_Vendor(request):
    context ={
            'vendor' : None,
        }
    try:
        vendor = Vendor.objects.get(user=request.user)
        context['vendor'] = vendor  #type:ignore
    except:
        pass
    return context

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user = request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)