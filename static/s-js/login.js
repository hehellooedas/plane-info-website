var csrf_token = $("[name='_csrf_token']").val();
var email1 = document.getElementById('username');
var password = document.getElementById('password');
var login1btn = document.getElementById("login-btn");
var sendbtn = document.getElementsByClassName('send-btn')[0];
var databack;
var time = 60;
var information;
var info = document.getElementsByClassName('info')[0];
var codefail = document.getElementsByClassName('codefail')[0];
sendbtn.addEventListener('click', function () {
	if (!reg.test(use.value)) {
		info.innerText = '输入格式错误';
	}
	else {
		information = { 'email': email1.value };
		$.ajax({
			type: "POST",
			url: '/login_ajax1',
			data: information,
			dataType: 'json',
			async: false,
			headers: { "X-CSRFToken": csrf_token },
			error: function (request) {
				alert("Connection error");
			},
			success: function (data) {
				if (data == '1') {
					sendbtn.className = "send-btn3";
					info.innerText = '你的用户未注册,请先去注册';
				}
				else {
					info.innerHTML = '<p>&nbsp</p>';
					sendbtn.className = "send-btn2";
					info.innerText = '邮件已发送,请注意查收';
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
				}
			}
		});
	}
})
// sendbtn.addEventListener('click', function () {
// });
login1btn.addEventListener('click', function () {
	if (databack == password.value) {
		$.ajax({

			type: "POST",
			url: '/login_ajax2',
			data: information,
			dataType: "text",
			async: false,
			headers: { "X-CSRFToken": csrf_token },
			error: function (request) {
				alert("Connection error");
			},
			success: function (data) {
				location.replace(data);
			}
		});
	}
	else { codefail.innerText = '验证码输入错误，请重新输入'; }
});
//正则表达式；
var reg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
var use = document.getElementById('username');
