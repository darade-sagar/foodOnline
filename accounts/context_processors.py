from vendor.models import Vendor

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