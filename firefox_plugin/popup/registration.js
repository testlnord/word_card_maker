
// browser.browserAction.onClicked.addListener {
//     console.log("WOW");
//     //browser.browserAction.setPopup("saveCard.html")
// });

var token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0OTIyNTI0MTcsImlhdCI6MTQ5MjI1MjExNywibmJmIjoxNDkyMjUyMTE3LCJpZGVudGl0eSI6Mn0.g1rcODsRYvqT-nEx1Za9mtheSq3HRWKvUTgGemvuK9E";

document.addEventListener("click", (e) => {
    if (e.target.name != "Forgot") {
    	return;
    }
	var password = document.getElementById('Password');
	var login = document.getElementById('Login');

	// var response = "nothing"; 
	// xhr = new XMLHttpRequest();
	// var url = "http://0.0.0.0:5000/auth";
	// // xhr.open("POST", url, true);
	// xhr.open("POST", url);
	// xhr.setRequestHeader("Content-type", "application/json");
	// xhr.onreadystatechange = function () { 
	//     if (xhr.readyState == 4 && xhr.status == 200) {
	//         var json = JSON.parse(xhr.responseText);
	//         response = json.access_token;
	//         alert(json);
	//     }
	// }
	// var data = JSON.stringify({username:"variance1", password:"1234"});
	// xhr.send(data);


	var xhr = new XMLHttpRequest();
	var url = "http://0.0.0.0:5000/auth";
	xhr.open("POST", url);
	xhr.setRequestHeader("Content-type", "application/json");


	// xhr.open('GET', 'http://0.0.0.0:5000/dict/translation?word=dog', true);
	// xhr.setRequestHeader("Authorization", "JWT " + token);
	xhr.onload = function() {
	 var responseText = xhr.responseText;
	 alert(responseText);
	 // process the response.
	};

	xhr.onerror = function() {
	  alert('There was an error!');
	};
	xhr.send();
	alert(xhr.responseText);


	// var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
	// xmlhttp.open("POST", "http://0.0.0.0:5000/auth");
	// xmlhttp.setRequestHeader("Content-Type", "application/json");
	// var token = xmlhttp.send(JSON.stringify({username:"variance", password:"1234"}));
	// // alert("Login: " + login.value + ", password: " + password.value);
	// alert(token);
	// // alert(response);
});


