$(document ).ready(function() {
  $('.dropdown ul>li').click(function(){
    $('.dropdown ul>li').each(function(){
      $(this).removeClass('drop-selected');
    });
    $(this).toggleClass('drop-selected');
    $('.dropdown>span').text($(this).attr("val"))
  });
});