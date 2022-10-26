function set_btn_status() {
  var radios = document.getElementsByName("uo");

  for (var i = 0; i < radios.length; i++) {
    console.log(radios)
    if (radios[i].checked) {
      console.log(radios[i].checked)
      var checked_value = radios[i].value;
      if (checked_value) {
        document.getElementById('submit_button').disabled = false;
      } else {
        document.getElementById('submit_button').disabled = true;
      }
      break;
    }

  }
}

var countDownDate = new Date("Nov 5, 2022 15:37:25").getTime();
var x = setInterval(function () {
  var now = new Date().getTime();
  var distance = countDownDate - now;
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);
  document.getElementById("vt").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
  if (distance < 0) {
    clearInterval(x);
    document.getElementById("vt").innerHTML = "EXPIRED";
  }
}, 1000);