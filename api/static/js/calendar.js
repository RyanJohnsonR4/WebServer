function tableText(tableCell) {
  var day = "";
  if (parseInt(tableCell.innerHTML) < 10){
    day += "0";
  }
  day+=tableCell.innerHTML.toString();
  window.location.href = (window.location.href.substring(0,window.location.href.indexOf("calendar")+8) + "/" + "05" + day +  "2016");
}
