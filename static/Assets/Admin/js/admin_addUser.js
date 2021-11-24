function validateForm() {
  debugger;
  // e.preventDefault();
  var x = document.forms["order_form"]["userAccountName"].value;
  var y = document.forms["order_form"]["userUserName"].value;
  var z = document.forms["order_form"]["userPassword"].value;
  var z1 = document.forms["order_form"]["userRePassword"].value;

  if (x == "") {
    document.getElementById("userAccountName").style.border = "3px solid red";
    document.getElementById("userAccountName").style.backgroundColor =
      "lightpink";

    document.getElementById("inputFields_miss").style.display = "block";
  }
  if (y == "") {
    document.getElementById("userUserName").style.border = "3px solid red";
    document.getElementById("userUserName").style.backgroundColor = "lightpink";
    document.getElementById("inputFields_miss").style.display = "block";
  }
  if (z == "") {
    document.getElementById("userPassword").style.border = "3px solid red";
    document.getElementById("userPassword").style.backgroundColor = "lightpink";
    document.getElementById("inputFields_miss").style.display = "block";
  }
  if (z1 == "") {
    document.getElementById("userRePassword").style.border = "3px solid red";
    document.getElementById("userRePassword").style.backgroundColor =
      "lightpink";
    document.getElementById("inputFields_miss").style.display = "block";
  } else {
    document.getElementById("userAccountName").style = "none";
    document.getElementById("userUserName").style = "none";
    document.getElementById("userPassword").style = "none";
    document.getElementById("userRePassword").style = "none";
    document.getElementById("inputFields_miss").style = "none";
  }
}
// });
