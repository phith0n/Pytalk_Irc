function addword(msg, uname, word, time){
	if (time) {
		time = "(" + time + ")";
	}else{
		time = '';
	}
	return msg + uname + time + " : " + word + "\n ";
}

function TimeToStr(nS) { 
	return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " "); 
} 

$("#send").click(function(){
	var sendbox = $("#sendbox").val();
	if (! sendbox || $("#sendbox").get(0).disabled) {
		return ;
	};
	$.post(root + "msg/", {
		'msg': sendbox
	}, function(data){
		var recvbox = ' ';
		var json = JSON.parse(data);
		if (json['num'] !== 0) {
			addword(recvbox, "错误", json['msg']);
		}else{
			for (var i = json['msg'].length - 1; i >= 0; i--) {
				recvbox = addword(recvbox, json['msg'][i]['uname'], json['msg'][i]['msg'], json['msg'][i]['time']);
			};
			$("#recvbox").val(recvbox);
			$("#sendbox").val('').focus();
		}
	})
})
$("document").ready(function(){
	getMsg();
	var timer = setInterval(function(){
		getMsg();
	}, 1000);
	$("#log").click(function(){
		if ($(this).attr("name") == 'log-close') {
			clearInterval(timer);
			showLog();
			$(this).val("关闭记录").attr("name", "log-open");
			$("#recvbox").css("overflow", "auto");
			$("#sendbox").get(0).disabled = true;
		}else{
			getMsg();
			timer = setInterval(function(){
				getMsg();
			}, 1000);
			$(this).val("查看记录").attr("name", "log-close");
			$("#recvbox").css("overflow", "hidden");
			$("#sendbox").get(0).disabled = false;
			$("#sendbox").focus();
		}
		
	})
})

document.onkeydown = function(e)
{
    var e=e||event;
    var currKey=e.keyCode||e.which||e.charCode;
    if (e.ctrlKey && (currKey == 13 || currKey == 10)) {
    	$("#send").click();
    };
}

function showLog(){
	$.get(root + "log/", {}, function(data){
		var recvbox = ' ';
		var json = JSON.parse(data);
		if (json['num'] === 0) {
			for (var i = json['msg'].length - 1; i >= 0; i--) {
				var time = TimeToStr(json['msg'][i]['time']);
				recvbox = addword(recvbox, json['msg'][i]['uname'], 
					json['msg'][i]['msg'], time);
			};
			$("#recvbox").val(recvbox);
		};
	})
}

function getMsg(){
	$.get(root + "msg/", {}, 
		function(data){
			var recvbox = ' ';
			var json = JSON.parse(data);
			if (json['num'] !== 0) {
				addword(recvbox, "错误", json['msg']);
			}else{
				for (var i = json['msg'].length - 1; i >= 0; i--) {
					recvbox = addword(recvbox, json['msg'][i]['uname'], json['msg'][i]['msg'], json['msg'][i]['time']);
				};
				$("#recvbox").val(recvbox);
			}
	})
}