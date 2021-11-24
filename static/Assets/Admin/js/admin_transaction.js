$(document).ready(function () {
  $("#example").DataTable();

  // date Validation

  $("#end-date-input").change(function () {
    debugger;
    var startDate = document.getElementById("start-date-input").value;
    var endDate = document.getElementById("end-date-input").value;

    if (Date.parse(startDate) > Date.parse(endDate)) {
      document.getElementById("inputFields_miss").style.display = "block";
      document.getElementById("EndDate").value = "";
    } else {
      document.getElementById("inputFields_miss").style.display = "none";
    }
  });
});
