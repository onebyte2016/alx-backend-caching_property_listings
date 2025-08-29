from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from django.shortcuts import render
from .utils import get_all_properties

# Cache response for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    properties = Property.objects.all().values("id", "title", "description", "price", "location", "created_at")
    return JsonResponse(list(properties), safe=False)



def property_list(request):
    properties = get_all_properties()
    return render(request, 'properties/property_list.html', {'properties': properties})
