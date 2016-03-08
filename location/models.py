from django.db import models
from django.db.models import signals
from django.core.exceptions import ValidationError
import apiclient
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from hashlib import md5

TABLE_ID = "1xj00bme-y6KfJHn8GV75XWf5YokIU2YyT4ZvOz8J"
application_secrets = "client_secrets.json"
scopes = ['https://www.googleapis.com/auth/fusiontables', 'https://www.googleapis.com/auth/fusiontables.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name(application_secrets, scopes)
http_auth = credentials.authorize(Http())
service = apiclient.discovery.build("fusiontables", "v2", http=http_auth)

class DuplicateError(Exception):
	pass

def delete_from_fusion_table(sender, instance, **kwargs):
	"""deletes row from fusion table after deleted from sqlite db"""
	address_hash = md5(instance.address.encode('utf-8')).hexdigest()
	select_sql = "SELECT rowid FROM %s WHERE AddressHash='%s'" % (TABLE_ID, address_hash)
	query_response = service.query().sql(sql = select_sql).execute()
	if "rows" not in query_response:
		return # not in fusion table!
	rowid = query_response["rows"][0][0]
	delete_sql = "DELETE FROM %s WHERE rowid='%s'" % (TABLE_ID, rowid)
	service.query().sql(sql = delete_sql).execute()

def add_to_fusion_table(sender, instance, **kwargs):
	"""saves to fusion tables before saving to sqlite3 UNLESS there is a duplicate"""
	address_hash = md5(instance.address.encode('utf-8')).hexdigest()#use hash of address to detect duplicaes
	select_sql = "SELECT rowid FROM %s WHERE AddressHash='%s'" % (TABLE_ID, address_hash)
	query_response = service.query().sql(sql = select_sql).execute()
	if "rows" in query_response:
		raise DuplicateError("Duplicate addresses aren't allowed in fusion tables") #DUPLICATE
	insert_sql = "INSERT INTO %s (Address, Coordinates, AddressHash) VALUES ('%s', '%f, %f', '%s')" % (TABLE_ID, instance.address, instance.latitude, instance.longitude, address_hash)
	service.query().sql(sql = insert_sql).execute()

def validate_lat_in_range(value):
	"""validates this is an in range latitude value"""
	_validate_in_range(value, -90, 90)

def validate_lng_in_range(value):
	"""validates this is an in range longitude value"""
	_validate_in_range(value, -180, 180)

def _validate_in_range(value, min_num, max_num):
	if value < min_num or value > max_num:
		raise ValidationError("%s is not within valid range" % value)

class Location(models.Model):
	address = models.CharField(max_length = 200)
	latitude = models.FloatField(validators = [validate_lat_in_range])
	longitude = models.FloatField(validators = [validate_lng_in_range])

	def format_for_js(self):
		return {"latitude": self.latitude, "longitude": self.longitude, "address": self.address}

signals.pre_save.connect(add_to_fusion_table, sender = Location)
signals.post_delete.connect(delete_from_fusion_table, sender = Location)