function addressType() {
  if (document.getElementById("lot_plan").checked) {
    console.log("hello");
    $(".Addressdiv").css("display", "none");
    $(".lotplandiv").css("display", "block");
  } else if (document.getElementById("Address").checked) {
    $(".Addressdiv").css("display", "block");
    $(".lotplandiv").css("display", "none");
  }
}

function validateForm() {
  debugger;
  if (document.getElementById("lot_plan").checked == true) {
    var form_lotNumber = document.forms["order_form"]["lotNumber"].value;
    var form_planType = document.forms["order_form"]["planType"].value;
    var form_planNumber = document.forms["order_form"]["planNumber"].value;

    if (form_lotNumber == "") {
      document.getElementById("lot_Number").style.border = "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    }
    if (form_planType == "Choose Plan Type") {
      document.getElementById("plan_Type").style.border = "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    }
    if (form_planNumber == "") {
      document.getElementById("planNumber").style.border = "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    } else {
      document.getElementById("lot_Number").style.border = "none";
      document.getElementById("plan_Type").style.border = "none";
      document.getElementById("planNumber").style.border = "none";
      document.getElementById("inputFields_miss").style.display = "none";
      return true;
    }
  } else if (document.getElementById("Address").checked == true) {
    var form_propertyAddressPostcode =
      document.forms["order_form"]["propertyAddressPostcode"].value;
    var form_propertyAddressStreetNumber =
      document.forms["order_form"]["propertyAddressStreetNumber"].value;
    var form_propertyAddressStreetName =
      document.forms["order_form"]["propertyAddressStreetName"].value;
    var form_propertyAddressSuburb =
      document.forms["order_form"]["propertyAddressSuburb"].value;

    if (form_propertyAddressPostcode == "") {
      document.getElementById("propertyAddressPostcode").style.border =
        "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    }
    if (form_propertyAddressStreetNumber == "") {
      document.getElementById("propertyAddressStreetNumber").style.border =
        "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    }
    if (form_propertyAddressStreetName == "") {
      document.getElementById("propertyAddressStreetName").style.border =
        "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    }
    if (form_propertyAddressSuburb == "") {
      document.getElementById("propertyAddressSuburb").style.border =
        "3px solid red";
      document.getElementById("inputFields_miss").style.display = "block";
    } else {
      document.getElementById("propertyAddressStreetNumber").style.border =
        "none";
      document.getElementById("propertyAddressStreetName").style.border =
        "none";
      document.getElementById("propertyAddressSuburb").style.border = "none";
      document.getElementById("propertyAddressPostcode").style.border = "none";
      document.getElementById("inputFields_miss").style.display = "none";
      return true;
    }
  }
}
function clickFunction() {
  document.getElementById("myForm").addEventListener("submit", (e) => {
    e.preventDefault();
  });
  if (validateForm() == true) {
    var section66 = false;
    var sewerServiceDiagram = false;
    var serviceLocationPrint = false;
    var buildingOverOrAdjacentToSewer = false;
    var specialMeterReading = false;
    var section88G = false;

    $.each($("input.checkbx_btn:checked"), function () {
      if ($(this).val() == "Section 66") {
        section66 = true;
      }
      if ($(this).val() == "Service Location Print") {
        serviceLocationPrint = true;
      }
      if ($(this).val() == "Building Over Or Adjacent To Sewer") {
        buildingOverOrAdjacentToSewer = true;
      }
      if ($(this).val() == "Special Meter Reading") {
        specialMeterReading = true;
      }
      if ($(this).val() == "Section 88G") {
        section88G = true;
      }
      if ($(this).val() == "Sewer Service Diagram") {
        sewerServiceDiagram = true;
      }
    });

    var of_lotNumber,
      of_planType,
      of_planNumber,
      of_sectionNumber,
      of_otherReferences,
      of_propertyUnitNumber,
      of_propertyAddressPostcode,
      of_propertyAddressStreetNumber,
      of_propertyType,
      of_propertyAddressStreetName,
      of_propertyAddressSuburb,
      of_applicantReferenceNumber,
      of_customerName;

    of_customerName = document.forms["order_form"]["customerName"].value;
    of_applicantReferenceNumber =
      document.forms["order_form"]["applicantReferenceNumber"].value;
    if (document.getElementById("lot_plan").checked == true) {
      of_lotNumber = document.forms["order_form"]["lotNumber"].value;
      of_planType = document.forms["order_form"]["planType"].value;
      of_planNumber = document.forms["order_form"]["planNumber"].value;
      of_sectionNumber = document.forms["order_form"]["sectionNumber"].value;
      of_otherReferences =
        document.forms["order_form"]["otherReferences"].value;

      order_data = {
        lotNumber: of_lotNumber,
        planType: of_planType,
        planNumber: of_planNumber,
        sectionNumber: of_sectionNumber,
        otherReferences: of_otherReferences,
        customerName: of_customerName,
        applicantReferenceNumber: of_applicantReferenceNumber,
        section66: section66,
        sewerServiceDiagram: sewerServiceDiagram,
        serviceLocationPrint: serviceLocationPrint,
        buildingOverOrAdjacentToSewer: buildingOverOrAdjacentToSewer,
        specialMeterReading: specialMeterReading,
        section88G: section88G,
      };
      console.log("Data is " + JSON.stringify(order_data));
      return true;
    }

    if (document.getElementById("Address").checked == true) {
      of_propertyAddressPostcode =
        document.forms["order_form"]["propertyAddressPostcode"].value;
      of_propertyAddressStreetNumber =
        document.forms["order_form"]["propertyAddressStreetNumber"].value;
      of_propertyAddressStreetName =
        document.forms["order_form"]["propertyAddressStreetName"].value;
      of_propertyAddressSuburb =
        document.forms["order_form"]["propertyAddressSuburb"].value;
      of_propertyType = document.forms["order_form"]["propertyType"].value;
      of_propertyUnitNumber =
        document.forms["order_form"]["propertyUnitNumber"].value;

      order_data = {
        propertyAddressPostcode: of_propertyAddressPostcode,
        propertyAddressStreetNumber: of_propertyAddressStreetNumber,
        propertyAddressStreetName: of_propertyAddressStreetName,
        propertyAddressSuburb: of_propertyAddressSuburb,
        propertyType: of_propertyType,
        propertyUnitNumber: of_propertyUnitNumber,
        customerName: of_customerName,
        applicantReferenceNumber: of_applicantReferenceNumber,
        section66: section66,
        sewerServiceDiagram: sewerServiceDiagram,
        serviceLocationPrint: serviceLocationPrint,
        buildingOverOrAdjacentToSewer: buildingOverOrAdjacentToSewer,
        specialMeterReading: specialMeterReading,
        section88G: section88G,
      };
      console.log("Data is " + JSON.stringify(order_data));
      return true;
    }

    // console.log("Data is " + JSON.stringify(order_data));
  }
}

//   $.ajax({
//     type: "POST",
//     async: false,
//     url: api_url,
//     data: JSON.stringify(order_data),
//     contentType: "application/json; charset=utf-8",
//     success: function (response) {

//         result = response;
//         if(result.Validate == true) {
//           document.getElementById("fail_alert").style.display="none";
//           document.getElementById("success_alert").style.display="block";
//           document.getElementById("confirm_order_div").style.display="block";
//         }
//          else if(result.Validate==false){
//           document.getElementById("fail_alert").style.display="block";
//         }

//     },
//     error: function (textStatus, errorThrown, response) {
//         alert(errorThrown);
//     }
// });

function orderId_cfm() {
  // window.location.reload();
  document.getElementById("orderId_div").style.display = "block";
}
function show() {
  if (clickFunction()) {
    document.getElementById("success_alert").style.display = "block";
    var sum = document.getElementById("sumary_div");
    sum.style.display = "block";
  } else {
    console.log("hi am false");
  }
}
function validate_prod_btn_fn() {
  var favorite = [];
  document.getElementById("order_summary").style.display = "block";

  //$.each($("input[name='drone']:checked"), function () {
  $.each($("input.checkbx_btn:checked"), function () {
    favorite.push($(this).val());
  });

  var order_details_str = `<ol> style="margin-right:65px;"`;
  if (favorite.length == 0) {
    order_details_str +=
      `<span style="color: red">` + "you don't hava any item" + `</span>`;
  } else {
    for (i = 0; i < favorite.length; i++) {
      order_details_str += `<li>` + favorite[i] + `</li>`;
    }
  }

  order_details_str += `</ol>`;

  document.getElementById("result").innerHTML = order_details_str;
}
