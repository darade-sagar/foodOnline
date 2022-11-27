from vendor.models import Vendor

def get_Vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    context ={
        'vendor' : vendor,
    }
    return context