angular.module('sherpanyapp')
.controller("navController", ["$scope", "LocationService", function($scope, LocationService) {
	$scope.io = false;
	$scope.clearData = function(){
		$scope.io = true;
		LocationService.clear().then(function(resp){
			$scope.io = false;
		});
	}
}]);