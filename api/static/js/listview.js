function updateCompletion(check,x,y,z){
  alert("WORKING");
  var url = x;
  var completed = y;
  var id = z;
  var oReq = new XMLHttpRequest();

  if (check.checked){
    oReq.open("PUT",url+"/api/v2/edit-note/"+id+"/"completed"/True",false);
    oReq.send("WHAT");
  }
  else{
    oReq.open("PUT",url+"/api/v2/edit-note/"+id+"/"completed"/False",false);
    oReq.send("WHAT");
  }
}
