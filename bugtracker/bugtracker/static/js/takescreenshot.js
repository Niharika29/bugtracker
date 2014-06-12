function capture() {
	$('body').html2canvas({
		onrendered: function(canvas) {
			$('#img').val(canvas.toDataURL('image/png'));
			document.getElementById('bug-form').submit();
		}
	});
}
