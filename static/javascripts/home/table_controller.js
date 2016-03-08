angular.module('sherpanyapp')
.controller("tableController", ["$scope", "LocationService", "NgTableParams", function($scope, LocationService, NgTableParams) {
	$scope.locationData = LocationService.data
	$scope.tableParams = new NgTableParams({
		count: 5
	}, {
		counts: [],
		paginationMaxBlocks: 13,
		paginationMinBlocks: 2,
		dataset: $scope.locationData.locations
	});
	$scope.$on('locationsChanged', function(event, args) {
		//reloads table when locations have changed
		$scope.tableParams.reload();
	});
}]);