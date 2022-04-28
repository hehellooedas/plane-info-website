var username=document.getElementById("username");
var password=document.getElementById("password");
var login1btn=document.getElementById("login-btn");
var sendbtn=document.getElementsByClassName('send-btn')[0];
var time=60;
   sendbtn.addEventListener('click',function(){
	   sendbtn.value="等待"+time+"s";
	   sendbtn.className=".send-btn2";
	   var ss=setInterval(function(){
		    time--;
			sendbtn.className="send-btn2";
			sendbtn.value="等待"+time+"s";
			if(time===0){
				sendbtn.value="发送";
				sendbtn.className=".send-btn";
				clearInterval(ss);
			}
	   },1000);
   })
   login1btn.addEventListener('click',function(){
	$.ajax({
		cache: true,
		type: "POST",
		url:'',
		data:$("#form-sign").serialize(),
		dataType:'json',
		async: false,
		error: function(request) {
			alert("Connection error");
		},
		success: function(data) {
                 
		}
	});
   });