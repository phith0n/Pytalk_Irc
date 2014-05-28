function addword(msg, uname, word, time){
	if (time) {
		time = "(" + time + ")";
	}else{
		time = '';
	}
	return msg + uname + time + " : " + word + "<br /> ";
}

function TimeToStr(nS) { 
	return new Date(parseInt(nS) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " "); 
} 

$("#send").click(function(){
	var sendbox = $("#sendbox").val();
	if (! sendbox || $("#sendbox").get(0).disabled) {
		return ;
	};
	if (sendbox.length > 128) {
		alert("太长啦，分多条发送吧~");
		return ;
	};
	$.post(root + "msg/", {
		'msg': sendbox, 
		'formhash': $("#formhash").val()
	}, function(data){
		var recvbox = ' ';
		var json = JSON.parse(data);
		if (json['num'] !== 0) {
			addword(recvbox, "错误", json['msg']);
		}else{
			for (var i = json['msg'].length - 1; i >= 0; i--) {
				recvbox = addword(recvbox, json['msg'][i]['uname'], json['msg'][i]['msg'], json['msg'][i]['time']);
			};
			if($("#recvbox").html() == recvbox){
				scrollDown();
				return ;
			}
			$("#recvbox").html(recvbox);
			scrollDown();
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
		$("#pause").click();
		if ($("#pause").attr("name") == 'pause-off') {
			showLog();
		}else{
			$("#sendbox").focus();
		}
	});
	$("#pause").click(function(){
		if ($(this).attr("name") == 'pause-on') {
			clearInterval(timer);
			$(this).val("继续聊天").attr("name", "pause-off");
			$("#sendbox").get(0).disabled = true;
		}else{
			clearInterval(timer);
			getMsg();
			timer = setInterval(function(){
				getMsg();
			}, 1000);
			$(this).val("暂停聊天").attr("name", "pause-on");
			$("#sendbox").get(0).disabled = false;
			$("#sendbox").focus();
		}
	})
})

function ajaxFileUpload()
{
	$("#inputupload").click().change(function(){
		$.ajaxFileUpload
	     (
	       {
	        url:root + 'file/', //你处理上传文件的服务端
	        secureuri:false,
	        fileElementId:'inputupload',
	        dataType: 'JSON',
	        success: function (data)
	      	{
	      		var json = JSON.parse(data);
	      		if (json['num'] > 0) {
	      			alert(json['msg']);
	      			return ;
	      		};
	      		getMsg();
	      	}
	       }
	     )
	})
	return false;
}

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
			$("#recvbox").html(recvbox);
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
				$("#recvbox").html(recvbox);
				scrollDown();
			}
	})
}

function scrollDown(){
	$("#recvbox").scrollTop( $('#recvbox')[0].scrollHeight );
}

function showimg(t){
  	var imgurl = $(t).attr("title");
	$.fancybox.open({
		href: imgurl,
		openEffect : 'elastic',
		openSpeed  : 150,

		closeEffect : 'elastic',
		closeSpeed  : 150,

		helpers : {
			overlay : null
		},
	});
}