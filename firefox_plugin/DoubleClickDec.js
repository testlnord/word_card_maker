//document.body.style.border = "5px solid blue";
var html = "";
var surroundings = "";
var currentDiv = null;

function onError(error) {
  console.log(`Error: ${error}`);
}

function onGot(item) {
  var color = "blue";
  if (item.color) {
    color = item.color;
  }
  document.body.style.border = "10px solid " + color;
}

var getting = browser.storage.local.get("color");
getting.then(onGot, onError);

var myPort = browser.runtime.connect({name:"port-from-dblclick"});
myPort.postMessage({greeting: "hello from content script"});

myPort.onMessage.addListener(function(m) {
  console.log("In content script, received message from background script: ");
  console.log(m.message);
  if (m.message === "lumos!") {
      currentDiv.style.background = "blue";
  }
});


function handleDoubleClick() {
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i)
                    .cloneContents());
            }
            html = container.innerHTML;
            surroundings = sel.getRangeAt(0).startContainer.parentNode.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange()
                .htmlText;
            //surroundings = document.selection.createRange().parentElement().innerHTML;

        }
    }

    var divf = document.createElement("div");
    divf.style.width = "100px";
    divf.style.height = "fit-content";
    divf.style.background = "red";
    divf.style.color = "white";
    divf.style.visibility = "visible";
    divf.innerHTML = html + "\nTranslation" + surroundings;
    divf.style.position = 'absolute';

    var scroll = document.documentElement.scrollTop || document.body.scrollTop;

    divf.style.top = scroll + 10 + 'px';

    myPort.postMessage({message: "new card!"});
    if (document.body.contains(currentDiv)) {
        document.body.replaceChild(divf, currentDiv);
        currentDiv = divf;
    } else {
      currentDiv = document.body.appendChild(divf);
    }

    //console.log(html);
    var text = String(html);
    console.log(text);
    //console.log(html.stripTags());
};


window.addEventListener("dblclick",
    function() {
        handleDoubleClick()
    }, false);


