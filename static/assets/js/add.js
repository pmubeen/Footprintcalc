$("#food").hide();
$("#energy").hide();
$("#water").hide();
$("#housing").hide();
$("#consumer").hide();
$("#electronics").hide();
$("#household").hide();
var food = null;
var apparel = null;
var electronics = null;
var household = null;
function checkField() {
  setInterval(function () {
    food = [
      $("#meat").val(),
      $("#dairy").val(),
      $("#bread").val(),
      $("#veggies").val(),
      $("#snacks").val(),
    ];
    apparel = [$("#clothes-no").val(), $("#shoes-no").val()];
    electronics = [$("#phone-no").val(), $("#comp-no").val()];
    household = [$("#decor-no").val(), $("#appliance-no").val()];
    if (
      ($("#trans-dist").val() == "" &&
        food.includes("") &&
        $("#energy-use").val() == "" &&
        $("#water-use").val() == "" &&
        $("#peep-no").val() == "" &&
        apparel.includes("") &&
        electronics.includes("") &&
        household.includes("")) ||
      $("#date").val() == ""
    ) {
      document.querySelector("#submit").disabled = true;
    } else if (
      $("#trans-dist").val() == "" &&
      food.includes("") &&
      $("#energy-use").val() == "" &&
      $("#water-use").val() == "" &&
      $("#peep-no").val() == "" &&
      apparel.includes("") &&
      electronics.includes("") &&
      household.includes("")
    ) {
      document.querySelector("#submit").disabled = true;
    } else {
      document.querySelector("#submit").disabled = false;
    }
  }, 100);
}
$(function () {
  $("#emission-sel").change(function () {
    switch ($("#emission-sel").val()) {
      case "Transport":
        $("#transport").show();
        $("#food").hide();
        $("#energy").hide();
        $("#water").hide();
        $("#housing").hide();
        $("#consumer").hide();

        $("#food").find("input").val("");
        $("#energy").find("input").val("");
        $("#water").find("input").val("");
        $("#housing").find("input").val("");
        $("#consumer").find("input").val("");
        break;
      case "Food":
        $("#transport").hide();
        $("#food").show();
        $("#energy").hide();
        $("#water").hide();
        $("#housing").hide();
        $("#consumer").hide();

        $("#transport").find("input").val("");
        $("#energy").find("input").val("");
        $("#water").find("input").val("");
        $("#housing").find("input").val("");
        $("#consumer").find("input").val("");
        break;
      case "Energy":
        $("#transport").hide();
        $("#food").hide();
        $("#energy").show();
        $("#water").hide();
        $("#housing").hide();
        $("#consumer").hide();

        $("#transport").find("input").val("");
        $("#food").find("input").val("");
        $("#water").find("input").val("");
        $("#housing").find("input").val("");
        $("#consumer").find("input").val("");
        break;
      case "Water":
        $("#transport").hide();
        $("#food").hide();
        $("#energy").hide();
        $("#water").show();
        $("#housing").hide();
        $("#consumer").hide();

        $("#transport").find("input").val("");
        $("#food").find("input").val("");
        $("#energy").find("input").val("");
        $("#housing").find("input").val("");
        $("#consumer").find("input").val("");
        break;
      case "Housing":
        $("#transport").hide();
        $("#food").hide();
        $("#energy").hide();
        $("#water").hide();
        $("#housing").show();
        $("#consumer").hide();

        $("#transport").find("input").val("");
        $("#food").find("input").val("");
        $("#energy").find("input").val("");
        $("#water").find("input").val("");
        $("#consumer").find("input").val("");
        break;
      case "Consumer Goods":
        $("#transport").hide();
        $("#food").hide();
        $("#energy").hide();
        $("#water").hide();
        $("#housing").hide();
        $("#consumer").show();

        $("#transport").find("input").val("");
        $("#food").find("input").val("");
        $("#energy").find("input").val("");
        $("#water").find("input").val("");
        $("#housing").find("input").val("");
        break;
      default:
        $("#transport").hide();
        $("#food").hide();
        $("#energy").hide();
        $("#water").hide();
        $("#housing").hide();
        $("#consumer").hide();
    }
  });
});
$(function () {
  $("#consume-sel").change(function () {
    switch ($("#consume-sel").val()) {
      case "Apparel":
        $("#apparel").show();
        $("#electronics").hide();
        $("#household").hide();
        break;
      case "Electronics":
        $("#apparel").hide();
        $("#electronics").show();
        $("#household").hide();
        break;

      case "Household":
        $("#apparel").hide();
        $("#electronics").hide();
        $("#household").show();
    }
  });
});
checkField();
