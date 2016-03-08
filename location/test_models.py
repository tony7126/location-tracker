from django.test import TestCase
from django.core.exceptions import ValidationError
from location.models import Location, validate_lat_in_range, validate_lng_in_range, service
from unittest.mock import MagicMock

class LocationTestCase(TestCase):
	def setUp(self):
		self.l = Location.objects.create(address = "3726 W. Columbia", latitude = 1.0, longitude = 1.0)
		self.l.save()
		service.query().sql = MagicMock(return_value = None)

	def test_format_for_js(self):
		"""test Location model helper function"""

		js_dict = self.l.format_for_js()
		assert "address" in js_dict
		assert js_dict["address"] == "3726 W. Columbia"
		assert "latitude" in js_dict
		assert js_dict["latitude"] == 1.0
		assert "longitude" in js_dict
		assert js_dict["longitude"] == 1.0

	def test_duplicates(self):
		"""test duplicate blocking for fusion tables"""

	def test_validators(self):
		"""test validators for lat/lng"""

		validate_lng_in_range(0)
		validate_lat_in_range(0)
		validate_lng_in_range(180)
		validate_lng_in_range(-180)
		validate_lat_in_range(90)
		validate_lat_in_range(-90)
		try:
			validate_lat_in_range(-91)
			assert False #means error wasnt thrown
		except ValidationError:
			pass
		try:
			validate_lat_in_range(91)
			assert False #means error wasnt thrown
		except ValidationError:
			pass

		try:
			validate_lng_in_range(-181)
			assert False #means error wasnt thrown
		except ValidationError:
			pass
		try:
			validate_lng_in_range(181)
			assert False #means error wasnt thrown
		except ValidationError:
			pass

	def tearDown(self):
		self.l.delete()
