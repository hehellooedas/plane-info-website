
var email1 = document.getElementById('username');
var password = document.getElementById('password');
var reg = document.getElementById("reg");//这里名字改了以下 
var sendbtn = document.getElementsByClassName('send-btn')[0];
var databack;
var time = 60;
var information;
// var info=document.getElementsByClassName('info')[0];这个去掉
var codefail=document.getElementsByClassName('codefail')[0];
sendbtn.addEventListener('click', function () {
	sendbtn.value = "等待" + time + "s";
	sendbtn.className = ".send-btn2";
	var ss = setInterval(function () {
		time--;
		sendbtn.className = "send-btn2";
		sendbtn.value = "等待" + time + "s";
		if (time === 0) {
			time = 60;
			sendbtn.value = "发送";
			sendbtn.className = ".send-btn";
			clearInterval(ss);
		}
	}, 1000);
	information = { 'email': email1.value, 'status': 'False' };
})
sendbtn.addEventListener('click', function () {
	$.ajax({
		type: "POST",
		url: '/login_ajax',
		data: information,
		dataType: 'json',
		async: false,
		error: function (request) {
			alert("Connection error");
		},
		success: function (data) {
			databack=data.Code;
			//这里的没注册消息就不要用啦 info.innerText=data.string;//没注册消息闪现
		}
	});
});
//注册成功和注册失败的消息闪现
reg.addEventListener('click', function () {
	if (databack == password.value) 
	{ information.status = 'True';
	  codefail.className='.codefail2';
	  codefail.innerText='注册成功';
    }
	else { codefail.innerText='验证码输入错误，请重新输入' }
	$.ajax({
		type: "POST",
		url: '/login_ajax',
		data: information,
		dataType: 'json',
		async: false,
	});
});