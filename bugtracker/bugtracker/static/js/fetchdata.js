$( document ).ready( function() {
	getloadtime();
	getdate();
	getos();
	getspeed();
	getbrowser();
});

function getloadtime() {
	var now = new Date().getTime();
	var page_load_time = now - performance.timing.navigationStart;
	$( '#id_loadtime' ).val(page_load_time);
}

function getdate() {
	var now = new Date();
	var dd = now.getDate();
	var mm = now.getMonth() + 1;
	var yy = now.getFullYear();
	if( dd < 10 ) { dd = '0' + dd; }
	if( mm < 10 ) { mm = '0' + mm; }
	$( '#id_date' ).val( yy + '-' + mm + '-' + dd );
}

function getos() {
	var OSName = "Unknown OS";
	if ( navigator.appVersion.indexOf( "Win" )!=-1 ) {
		OSName = "Windows";
	}
	else if ( navigator.appVersion.indexOf( "Mac" )!=-1 ) {
		OSName = "MacOS";
	}
	else if ( navigator.appVersion.indexOf( "X11" )!=-1 ) {
		OSName = "UNIX";
	}
	else if ( navigator.appVersion.indexOf( "Linux" )!= 1 ) {
		OSName = "Linux";
	}
	
	$( '#id_os' ).val( OSName );
}

function getbrowser() {
	var isOpera = !!window.opera || navigator.userAgent.indexOf( "OPR/" ) >= 0;
	var isFirefox = typeof InstallTrigger !== 'undefined';
	var isSafari = Object.prototype.toString.call( window.HTMLElement ).indexOf( 'Constructor' ) > 0;
	var isChrome = !!window.chrome && !isOpera;
	var isIE = false || !!document.documentMode;
	
	if( isOpera ) {
		$( '#id_browser' ).val( 'Opera' );
	}
	if( isFirefox ) {
		$( '#id_browser' ).val( 'Firefox' );
	}
	if( isSafari ) {
		$( '#id_browser' ).val( 'Safari' );
	}
	if( isChrome ) {
		$( '#id_browser' ).val( 'Chrome' );
	}
	if( isIE ) {
		$( '#id_browser' ).val( 'Internet Explorer' );
	}
}	
	
function getspeed() {
	var imageAddr = "http://oozie.org/wp-content/wallpapers/2013/09/Disney-World-Desktop-Wallpaper.jpg?n=" + Math.random();
	//var imageAddr = "http://i.imgur.com/lR6IUex.jpg?n=" + Math.random();
	var startTime, endTime;
	var downloadSize = 1234979;
	var download = new Image();
	startTime = ( new Date() ).getTime();
	download.src = imageAddr; 
	download.onload = function() { 
		endTime = ( new Date() ).getTime();
		showResults( startTime, endTime, downloadSize );
	}
}

function showResults( startTime, endTime, downloadSize ) {
	var duration = ( endTime - startTime )/1000;
	var bitsLoaded = downloadSize*8;
	var bps = ( bitsLoaded/duration ).toFixed(2);
	var kbps = ( bps/1024 ).toFixed(2);
	var mbps = ( kbps/1024 ).toFixed(2);
	$( '#id_netspeed' ).val( mbps );
}
