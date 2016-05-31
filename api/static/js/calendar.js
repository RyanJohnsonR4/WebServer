function tableText(tableCell, month) {
  var day = "";
  if (parseInt(tableCell.innerText) < 10){
    day += "0";
  }
  day+=tableCell.innerText.toString();
  window.location.href = (window.location.href.substring(0,window.location.href.indexOf("calendar")+8) + "/" + parseMonth(month) + day +  "2016");
}

function parseMonth(month){
  if (month == "January")
    return "01";
  if (month == "Febraury")
    return "02";
  if (month == "March")
    return "03";
  if (month == "April")
    return "04";
  if (month == "May")
    return "05";
  if (month == "June")
    return "06";
  if (month == "July")
    return "07";
  if (month == "August")
    return "08";
  if (month == "September")
    return "09";
  if (month == "October")
    return "10";
  if (month == "November")
    return "11";
  if (month == "December")
    return "12";
}
