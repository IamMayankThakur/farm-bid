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
		"itemname": $("input[name='itemName']").val(),
		"itemBasePrice": $("input[name='basePrice']").val(),
		"quantity": $("input[name='quantity']").val(),
		"itemCatName": $("input[name='category']").val()
	}
	console.log(request);
    sellerId = null;
	$.post(
		ip + "get_uid",
		{"username": $("input[name='username']").val()},
		function (response, success) {
			sellerId = response.userid;
		},
	);
    request.sellerId = sellerId;
	$.post(
		ip + "item",
		request,
		function (response, success) {
			resp = response;
			alert("Success");
		},
	);

}

function plot_graph() {
    prices = null;

    $.post(ip + "item-stats",
    {"item_name": $("input[name='itemName']").val()},
        function(data, success) {
            prices = data;
        }
    );

  xs = []
  ys = []
  for (int i=0; i<prices.length; i++) {
    xs.push(i+1);
    ys.push(prices[i]);
  }

  var trace1 = {
  x: xs,
  y: ys,
  type: 'scatter'
  };
  var data = [trace1];
  Plotly.newPlot('myDiv', data);
}