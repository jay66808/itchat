$(document).ready(function hov(){
	$(".reply").click(function huifu(){
		$(".reply_content").toggle();
	})

	$(".comment_reply").click(function reply(){
		$(".reply_content").toggle();
	})
	var lik=1;
	$(".like").click(function like(){
		if (lik) {
		$(".like").css("background","url(images/like2.gif)");
		lik=0;
		var alr=$(".alr_like");
		alr.show();
		alr.hide(3000);
	}
	else{
		$(".like").css("background","url(images/like.gif)");
		lik=1;
	}
	})
	var col=1;
	$(".collet").click(function collet(){
		
		if (col) {
			$(".collet").css("background","url(images/collet2.gif)");
			col=0;
			alert("已收藏")
		}
		else{
			$(".collet").css("background","url(images/collet.gif)");
			col=1;
		}
	})
	
	$(function(){
    $(".ce > li > a").click(function(){
	     $(this).addClass("xz").parents().siblings().children("a").removeClass("xz");
		 $(this).parents().siblings().children(".er").hide(300);
		 $(this).siblings(".er").toggle(300);
		 $(this).parents().siblings().children(".er > li > .thr").hide().parents().siblings().children(".thr_nr").hide();
		
	})
	
    $(".er > li > a").click(function(){
        $(this).addClass("sen_x").parents().siblings().children("a").removeClass("sen_x");
        $(this).parents().siblings().children(".thr").hide(300);	
	    $(this).siblings(".thr").toggle(300);	
	})

    $(".thr > li > a").click(function(){
	     $(this).addClass("xuan").parents().siblings().children("a").removeClass("xuan");
		 $(this).parents().siblings().children(".thr_nr").hide();	
	     $(this).siblings(".thr_nr").toggle();
	})
})



  $(".bd").hover(function(){
      $(this).siblings().hide();
    }) 
  $(".bd").mouseleave(function(){
	  $(this).siblings().show();
  })

	
})