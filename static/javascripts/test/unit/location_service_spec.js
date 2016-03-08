describe("mapController", function(){
	var $httpBackend, createController;
	beforeEach(module("sherpanyapp"));

	$scope = $injector.get('$scope');

	$httpBackend = $injector.get('$httpBackend');
	$httpBackend.when('GET', '/location')
		.respond({data: {locations: [{address: "3726 W. Columbia Lincolnwood, IL", latitude:2, longitude: 2}]}})

	var $controller = $injector.get('$controller');

	createController = function() {
		return $controller('mapController', {'$scope' : $rootScope.$new() });
	};

	it("should have one location in scope", function(){

	})

})

