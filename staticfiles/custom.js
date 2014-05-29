	$(function() {
		$( "#sortable" ).sortable();
		$( "#sortable" ).disableSelection();
	});

	$(".deleter").click(function () {
	/*$(".deleter").live("click", function() {
	 * */
	    $(this).parent("li").hide("slider", function () {
		$(this).remove();
				      });
	});


