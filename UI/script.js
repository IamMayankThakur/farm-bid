var app = angular.module('myApp', []);
var ip = "http://127.0.0.1/api/";
app.controller('testController', function ($scope, $http) {
	$scope.bids = [{
		'itemName': "name",
		'itemId': 12,
		'basePrice': 123,
		'sellerId': 1,
		'sellerName': "user2",
		'sellerRating': 3.3
	}]

	$scope.onBid = function() {
		var bidValue = prompt(" Place your Bid");
		request = {
			"buyerId": 1,
			"itemId": this.bid.itemId,
			"price": bidValue
		}
		$http.post(ip + "place_bid", request);
		// Create socket io connection
	}

	$scope.init = function () {
		$http.get(ip + "item")
		.then(function (response) {
			$scope.bids = response.data;
		})
	}
});


