document.body.style.border = "5px solid blue";
var html = "";

// function domRangeCreate() {
    // Найдем корневой контейнер
  //  var root = document.getElementById('ex2');
    // Найдем контейнеры граничных точек (в данном случае тестовые)
  //  var start = root.getElementsByTagName('h2')[0].firstChild;
   // var end = root.getElementsByTagName('p')[0].firstChild;
    //if (root.createRange) {
      // Создаем Range
    //  var rng = root.createRange();
      // Задаем верхнюю граничную точку, передав контейнер и смещение
     // rng.setStart(start, 3);
      // Аналогично для нижней границы
     // rng.setEnd(end, 10);
      // Теперь мы можем вернуть текст, который содержится в полученной области
     // return rng.toString();
    //} else {
     // return 'Вероятно, у вас IE8-, смотрите реализацию TextRange ниже';
    //}
  //}

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
    //self.postMessage(
      //  JSON.stringify({
        //    plain: window.getSelection()
          //      .toString(),
            //html: html
        //})
    //);
    console.log(html);
    //browser.contextMenus.create(
    //createProperties) // object
    //function() {...}  // optional function
};


window.addEventListener("dblclick",
    function() {
        handleDoubleClick()
    }, false);

