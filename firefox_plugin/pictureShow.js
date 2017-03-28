function pictureShow(request, sender, sendResponse) {
  removeEverything();
  insertPicture(request.pictureURL);
  browser.runtime.onMessage.removeListener(pictureShow);
}

/*
Remove every node under document.body
*/
function removeEverything() {
  while (document.body.firstChild) {
    document.body.firstChild.remove();
  }
}

/*
Given a URL to a card image, create and style an IMG node pointing to
that image, then insert the node into the document.
*/
function insertPicture(pictureURL) {
  var pictureImage = document.createElement("img");
  pictureImage.setAttribute("src", pictureURL);
  pictureImage.setAttribute("style", "width: 100vw");
  pictureImage.setAttribute("style", "height: 100vh");
  document.body.appendChild(pictureImage);
}

/*
Assign pictureShow() as a listener for messages from the extension.
*/
browser.runtime.onMessage.addListener(pictureShow);