function isNumeric(str){
   var allowedChars = "+0123456789";
   var isDigit=true;
   var char;
   for (i = 0; i  < str.length && isDigit == true; i++){
      char = str.charAt(i);
      if (allowedChars.indexOf(char) == -1)  isDigit = false;
      }
   return isDigit;
}

function isAlpha(str){
   str = str.toLowerCase();
   var allowedChars = "-: абвгдеёжзийклмнопрстуфхцчшщъыьэюя";
   var isal=true;
   var char;
   for (i = 0; i  < str.length && isal == true; i++){
      char = str.charAt(i);
      if (allowedChars.indexOf(char) == -1){
        isal = false;}
      }
   return isal;
}

function validateForm(){
  var phone = document.getElementById("phone").value;
  var address = document.getElementsByClassName("address");
  var place = document.getElementsByClassName("place");

  if (((phone.length<8)||(phone.length>12))||(!isNumeric(phone)))
  {
    alert("Неправильный номер телефона!");
    return false;
  }

  for(var i=0; i<address.length; i++){
    if(address[i].value.length<2){
      alert("Неправильно "+address[i].name+"!");
      return false;}
  }

  for(i=0; i<place.length; i++){
    if((isAlpha(place[i].value)==false)||(place[i].value.length<2)){
      alert("Неправильно "+place[i].name+"!");
      return false;}
  }
}

function checkEqual(){
  var pass = document.getElementsByName("password")[0].value;
  var cnfrm_pass = document.getElementsByName("cnfrm_psswd")[0].value;

  if(pass!==cnfrm_pass){
    alert("Пароль и пароль для подтверждения не совпадают");
    return false;
  }
}

function checkSelect(){
  var radio = document.getElementsByName("метод поиска")
  var byKeyword = radio[0].checked
  var byCategory = radio[1].checked
  var both = radio[2].checked
  var select = document.getElementsByTagName("select").category.value
  if((byCategory||both)&&(select=="")){
    alert("Пожалуйста, выберите категорию")
    return false;}
}
