from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from location.models import Location, DuplicateError
from django.core import serializers
import json

class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class LocationView(View):
	def get(self, request, *args, **kwargs):
		data = serializers.serialize("json", Location.objects.all())
		data = [l.format_for_js() for l in Location.objects.all()]
		return JsonResponse({"locations": data})

	def post(self, request, *args, **kwargs):
		location_dict = json.loads(request.body.decode("utf-8") )
		location = Location(**location_dict)
		try:
			location.save()
		except DuplicateError:
			return JsonResponse({"error": "Can't save duplicates"})
		return JsonResponse({"location": location.format_for_js()})


	def delete(self, request, *args, **kwargs):
		Location.objects.all().delete()
		return JsonResponse({"status": "success"})