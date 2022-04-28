
var login1btn=document.getElementById("login-btn");
var username=document.getElementById('username');
var password=document.getElementById('password');
var obj={
	email:'',
	status:''
};
var databack;
console.log(obj);
var sendbtn=document.getElementsByClassName('send-btn')[0];
var time=60;
       sendbtn.addEventListener('click',function(){
	   obj.email=username.value;
	   console.log(obj);
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
       $.ajax({
		cache: true,
		type: "POST",
		url:'',
		data:JSON.stringify(obj),//username=15194494354&password=aa  这样的
		dataType:'json',
		async: false,
		error: function(request) {
			alert("Connection error");
		},
		success: function(data) {
            databack=data;
		}
	});
   })
   login1btn.addEventListener('click',function(){
	obj.email=username.value;
	obj.status=password.value;
	if(obj.status===databack){
		obj.status="true";
	}
	console.log(obj);
	$.ajax({
		cache: true,
		type: "POST",
		url:'',
		data:JSON.stringify(obj),//username=15194494354&password=aa  这样的
		dataType:'json',
		async: false,
		error: function(request) {
			alert("Connection error");
		},
		success: function(data) {

		}
	});
   });