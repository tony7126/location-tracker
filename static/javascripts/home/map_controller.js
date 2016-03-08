var sherpanyApp = angular.module('sherpanyapp')
.controller("mapController", ["$scope", "NgMap", "LocationService", function($scope, NgMap, LocationService) {
	$scope.io = false;
	var geocoder = new google.maps.Geocoder;
	$scope.locData = LocationService.data; //set location data on scope to the service's
	$scope.$on('mapInitialized', function(event, evtMap) {
		var map = evtMap;
		google.maps.event.addListener(map, 'click', function(evt){
			var latLng = {lat: evt.latLng.lat(), lng: evt.latLng.lng()}
			$scope.io = true; //turn on IO flag (spinner is based on this)
			geocoder.geocode({"location": latLng}, function(results, status) {
				if (status === google.maps.GeocoderStatus.OK) {
					if (results[0]) { //only save address if location is valid!
						var locObj = {address: results[0].formatted_address, latitude: latLng.lat, longitude: latLng.lng};
						$scope.saveLocation(locObj);
						
					}
				} else {
					alert("Invalid location!")
					$scope.io = false;
				}

			})
		});

	});

	$scope.saveLocation = function(locObj){
		LocationService.save(locObj).then(function(resp){
			$scope.io = false;
			if (resp.hasOwnProperty('error')) {
				console.log(resp.error)
				alert("Error: " + resp.error);
			} else {
				alert("Address saved!");
			}
			
		});
	}
}]);