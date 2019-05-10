function init() {
  var submitButton = document.getElementById("submit");
  var addChapterTitleButton = document.getElementById("add_chapter_title");

  submitButton.onclick = checkMandatoryFields;
  addChapterTitleButton.onclick = addChapterTitle;
}


function checkMandatoryFields(e) {
//TODO: Fix this function
  var mandatoryFields = document.getElementsByClassName("required");
  for (var i = 0; i < mandatoryFields.length; i++) {
    if (mandatoryFields[i].value === "") {
      mandatoryFields[i].value = "You must enter a "
//      mandatoryFields[i].value = "You must enter a " + mandatoryField[i].name;
      mandatoryFields[i].setAttribute("class", "missing");
//      alert("Please fill out all mandatory fields");
      break;
    }
  }
}

/**
 * @param {String} HTML representing a single element
 * @return {Element}
 */
function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function addChapterTitle() {
  var template = document.querySelector("#chapter_title");
  var clone = document.importNode(template.content, true);

  var chapter_table = document.querySelector("#chapter_table");
  chapter_table.appendChild(clone);
// create new ChapterTitle element
// add element to correct position in HTML
}


window.onload = init;
