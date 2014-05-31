//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	next_fs = $(this).parent().next();
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			scale = 1 - (1 - now) * 0.2;
			current_fs.css({'transform': 'scale('+scale+')'});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
			$.post(root + 'login/', {
				'name': $("#name").val(), 
				'pass': hex_md5($("#pass").val())
			}, function(data){
				var json = eval('(' + data + ')');
				if (json['num'] !== 0) {
					alert(json['msg']);
					current_fs.show();
					current_fs.css({'opacity': '1', 'transform': 'scale(1)'});
				}else{
					location.href = root + 'show/';
				}
			})
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	return false;
})

