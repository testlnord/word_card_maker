/*
Called when the item has been created, or when creation failed due to an error.
We'll just log success/failure here.
*/
function onCreated(n) {
  if (browser.runtime.lastError) {
    console.log(`Error: ${browser.runtime.lastError}`);
  } else {
    console.log("Item created successfully");
  }
}

/*
Called when the item has been removed.
We'll just log success here.
*/
function onRemoved() {
  console.log("Item removed successfully");
}

/*
Called when there was an error.
We'll just log the error here.
*/
function onError(error) {
  console.log(`Error: ${error}`);
}

/*
Create all the context menu items.
*/
browser.contextMenus.create({
  id: "log-selection",
  title: "some_log",
  contexts: ["selection"]
}, onCreated);

browser.contextMenus.create({
  id: "remove-me",
  title: "wanna_remove",
  contexts: ["all"]
}, onCreated);

browser.contextMenus.create({
  id: "separator-1",
  type: "separator",
  contexts: ["all"]
}, onCreated);

browser.contextMenus.create({
  id: "showCard",
  type: "radio",
  title: "showCard",
  contexts: ["all"],
  checked: true
}, onCreated);

browser.contextMenus.create({
  id: "picturesque",
  type: "radio",
  title: "picturesque",
  contexts: ["all"],
  checked: false
}, onCreated);

browser.contextMenus.create({
  id: "separator-2",
  type: "separator",
  contexts: ["all"]
}, onCreated);

var checkedState = true;

browser.contextMenus.create({
  id: "check-uncheck",
  type: "checkbox",
  title: "check_me",
  contexts: ["all"],
  checked: checkedState
}, onCreated);

/*
Set a colored border on the document in the given tab.
Note that this only work on normal web pages, not special pages
like about:debugging.
*/
var blue = 'document.body.style.border = "5px solid blue"';
var green = 'document.body.style.border = "5px solid green"';

function borderify(tabId, color) {
  browser.tabs.executeScript(tabId, {
    code: color
  });
}


/*
 * A port to communicate with DoubleClickDec
*/
var portFromDoubleClickDec;
function connected(p) {
  portFromDoubleClickDec = p;
  portFromDoubleClickDec.postMessage({message: "hi there content script!"});
  portFromDoubleClickDec.onMessage.addListener(function(m) {
    console.log("In background script, received message from content script")
    console.log(m.message);
  });
}
browser.runtime.onConnect.addListener(connected);

/*
Toggle checkedState, and update the menu item's title
appropriately.
Note that we should not have to maintain checkedState independently like
this, but have to because Firefox does not currently pass the "checked"
property into the event listener.
*/
function updateCheckUncheck() {
  checkedState = !checkedState;
  if (checkedState) {
    browser.contextMenus.update("check-uncheck", {
      title: browser.i18n.getMessage("contextMenuItemUncheckMe"),
    });
  } else {
    browser.contextMenus.update("check-uncheck", {
      title: browser.i18n.getMessage("contextMenuItemCheckMe"),
    });
  }
}

/*
The click event listener, where we perform the appropriate action given the
ID of the menu item that was clicked.
*/
browser.contextMenus.onClicked.addListener(function(info, tab) {
  switch (info.menuItemId) {
    case "log-selection":
      console.log(info.selectionText);
      break;
    case "remove-me":
      var removing = browser.contextMenus.remove(info.menuItemId);
      removing.then(onRemoved, onError);
      break;
    case "picturesque":
      borderify(tab.id, blue);
      chosenPictureURL = browser.extension.getURL("pictures/card.jpg");
      browser.tabs.executeScript(null, { 
      file: "pictureShow.js" 
    });

    var gettingActiveTab = browser.tabs.query({active: true, currentWindow: true});
    gettingActiveTab.then((tabs) => {
      browser.tabs.sendMessage(tabs[0].id, {pictureURL: chosenPictureURL});
    });
      break;
    case "showCard":
      borderify(tab.id, green);
      portFromDoubleClickDec.postMessage({message: "lumos!"});
      break;
    case "check-uncheck":
      updateCheckUncheck();
      break;
  }
});

