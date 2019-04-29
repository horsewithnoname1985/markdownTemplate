function init() {
  var submitButton = document.getElementById("submit");
  submitButton.onclick = checkMandatoryFields;
}


function checkMandatoryFields(e) {
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

window.onload = init;