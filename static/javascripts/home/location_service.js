var sherpanyApp = angular.module('sherpanyapp')

sherpanyApp.factory("LocationService", ['$http', '$rootScope', function($http, $rootScope){
	var locations = [];
	var service = {

		//gets all locations in the database
		get: function() {
			return $http({
				method: 'GET',
				url: "/location", 
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				return {locations: resp.data.locations}
			}, function(error){
				return {error: error}
			});
		},

		// saves a new location
		save: function(data) {
			return $http({
				method: 'POST',
				url: "/location", 
				data: data,
				headers: {
    				'Content-Type': 'application/json'
				}
			}).then(function(resp) {
				if (resp.data.hasOwnProperty('error')) {
					return {error: resp.data.error}
				}
				locations.push(data);
				$rootScope.$broadcast('locationsChanged')
				return {location: data}
			}, function(resp){
				return {error: "Error processing request"}
			});
		},

		clear: function(){
			return $http({
				method: 'DELETE',
				url: "/location", 
			}).then(function(resp){
				locations.length = 0;
				$rootScope.$broadcast('locationsChanged')
				return {"status": "success"}
			}, function(error){
				return {"error": error}
			})
		},

		//stores locations locally
		data: {locations: locations} 

	}

	//initializes local in memory dataset
	service.get().then(function(resp){
		if (resp.locations !== undefined) {
			for (var i = 0; i < resp.locations.length; i++)
				service.data.locations.push(resp.locations[i])
			$rootScope.$broadcast('locationsChanged')
		}

	})
	return service; //replace with IG
}]);

