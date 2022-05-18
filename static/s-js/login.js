var email1 = document.getElementById('username');
var password = document.getElementById('password');
var login1btn = document.getElementById("login-btn");
var sendbtn = document.getElementsByClassName('send-btn')[0];
var databack;
var time = 60;
var information;
var info=document.getElementsByClassName('info')[0];
var codefail=document.getElementsByClassName('codefail')[0];
sendbtn.addEventListener('click', function () {
	sendbtn.value = "等待" + time + "s";
	sendbtn.className = "send-btn2";
	var ss = setInterval(function () {
		time--;
		sendbtn.value = "等待" + time + "s";
		if (time === 0) {
			time = 60;
			sendbtn.value = "发送";
			sendbtn.className = "send-btn3";
			clearInterval(ss);
		}
	}, 1000);
	information = { 'email': email1.value};
})
sendbtn.addEventListener('click', function () {
	$.ajax({
		type: "POST",
		url: '/login_ajax1',
		data: information,
		dataType: 'json',
		async: false,
		error: function (request) {
			alert("Connection error");
		},
		success: function (data) {
			databack=data.Code;
			info.innerText=data.string;//没注册消息闪现
		}
	});
});
login1btn.addEventListener('click', function () {
	if (databack == password.value) {
	$.ajax({
		type: "POST",
		url: '/login_ajax2',
		data: information,
		async: false,
		error: function (request) {
			alert("Connection error");
		},
		success: function (data) {
			location.href = data;
		}
	});
	}
	else { codefail.innerText='验证码输入错误，请重新输入'; }
});
//正则表达式；
  var reg=/^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
  var use=document.getElementById('username');
  use.addEventListener('blur',function(){
	  if(!reg.test(use.value))
	  {
		info.innerText='输入格式错误';
		sendbtn.className = "send-btn2";
	  }
	  else{
		sendbtn.className = "send-btn3";
		info.innerText='';
	  }
  })
