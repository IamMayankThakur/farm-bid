var app = angular.module('basepriceApp', []);
var ip = "http://127.0.0.1/api/";
app.controller('basepriceController', function ($scope, $http) {
	$scope.addItem = function () {
		console.log("ASas");
		request = {
			"sellerId": 1,
			"itemname": $scope.itemName,
			"itemBasePrice": $scope.basePrice,
			"quantity": $scope.quantity,
			"itemCatName": $scope.category
		}
		console.log(request);
	}
});

addItem = function () {
	request = {
		"sellerId": 1,
		"itemname": $("input[name='itemName']").val(),
		"itemBasePrice": $("input[name='basePrice']").val(),
		"quantity": $("input[name='quantity']").val(),
		"itemCatName": $("input[name='category']").val()
	}
	console.log(request);
	$.post(
		ip + "item",
		request,
		function (response, success) {
			resp = response;
			alert("Success");
		},
	);

}