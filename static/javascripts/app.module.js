var sherpanyApp = angular.module('sherpanyapp', ['ngMap', 'ngTable', 'ui.bootstrap'])
.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});