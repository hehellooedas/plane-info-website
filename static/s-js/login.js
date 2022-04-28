var email1=document.getElementById('username');
var password=document.getElementById('password');
var databack;
var login1btn=document.getElementById("login-btn");
var sendbtn=document.getElementsByClassName('send-btn')[0];
var time=60;
var information;
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
	   information = {'email':email1.value,'status':'False'};
   })
   sendbtn.addEventListener('click',function(){
	$.ajax({
		type: "POST",
		url:'/login_ajax',
		data:information,
		dataType:'json',
		async: false,
		error: function(request) {
			alert("Connection error");
		},
		success: function(data) {
            databack=data;
            if(databack==email1.value){information={'email':email1.value,'status':'True'};}
		}
	});
   });
    login1btn.addEventListener('click',function(){
	$.ajax({
		type: "POST",
		url:'/login_ajax',
		data:{'email':email1.value,'statu s':'True'},
		dataType:'json',
		async: false,
	});
   });
