
// browser.browserAction.onClicked.addListener {
//     console.log("WOW");
//     //browser.browserAction.setPopup("saveCard.html")
// });

document.addEventListener("click", (e) => {
    if (e.target.name != "Forgot") {
    	return;
    }
	var password = document.getElementById('Password');
	var login = document.getElementById('Login');
	alert("Login: " + login.value + ", password: " + password.value);
});