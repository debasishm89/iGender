$(document).ready(function(){
  $("#igender").blur(function(){
  var name = $("#igender").val();
      if(name != "")
      {
	$.post("http://www.i-gender.com/ai",{name:$("#igender").val()},
	function(data,status){
	    var obj = jQuery.parseJSON(data);
	    if(obj.gender == "male"){
document.getElementById('igender-result').innerHTML = '<img src="http://cdn1.iconfinder.com/data/icons/humano2/128x128/emblems/emblem-people.png">';
	  }
	  else{
document.getElementById('igender-result').innerHTML = '<img src="http://cdn1.iconfinder.com/data/icons/CrystalClear/128x128/kdm/user_female.png">';
	  }
    });
}
else{
alert("Please Enter a First Name");document.getElementById('name').focus();
}
});
});