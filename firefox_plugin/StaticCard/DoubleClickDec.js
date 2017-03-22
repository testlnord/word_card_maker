document.body.style.border = "5px solid blue";
var html = "";
var currentDiv = null;

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
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange()
                .htmlText;
        }
    }

    var divf = document.createElement("div");
    divf.style.width = "100px";
    divf.style.height = "100px";
    divf.style.background = "red";
    divf.style.color = "white";
    divf.style.visibility = "visible";
    divf.innerHTML = html;
    divf.style.position = 'absolute'

    var scroll = document.documentElement.scrollTop || document.body.scrollTop

    divf.style.top = scroll + 10 + 'px'

    myPort.postMessage({message: "new card!"})
    if (document.body.contains(currentDiv)) {
      document.body.replaceChild(divf, currentDiv);
      currentDiv = divf;
    } else {
      currentDiv = document.body.appendChild(divf);
    }

    console.log(html);
};

function handleKeyDown () {
  document.getElementById("divf").style.visibility = "visible";
}

window.addEventListener("dblclick",
    function() {
        handleDoubleClick()
    }, false);


