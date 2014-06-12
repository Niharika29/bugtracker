/*Project specific JavaScript*/
console.log('Hello there!');

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
	
	$( '#os' ).html( 'Detected Operating System is: ' + OSName );
}

function getbrowser() {
	var isOpera = !!window.opera || navigator.userAgent.indexOf( "OPR/" ) >= 0;
	var isFirefox = typeof InstallTrigger !== 'undefined';
	var isSafari = Object.prototype.toString.call( window.HTMLElement ).indexOf( 'Constructor' ) > 0;
	var isChrome = !!window.chrome && !isOpera;
	var isIE = false || !!document.documentMode;
	
	if( isOpera ) {
		$( '#browser' ).html( 'Detected Browser is: Opera' );
	}
	if( isFirefox ) {
		$( '#browser' ).html( 'Detected Browser is: Firefox' );
	}
	if( isSafari ) {
		$( '#browser' ).html( 'Detected Browser is: Safari' );
	}
	if( isChrome ) {
		$( '#browser' ).html( 'Detected Browser is: Chrome' );
	}
	if( isIE ) {
		$( '#browser' ).html( 'Detected Browser is: Internet Explorer(ugh!)' );
	}
}	
	
function getloadtime() {
	var now = new Date().getTime();
	var page_load_time = now - performance.timing.navigationStart;
	$( '#loadtime' ).html( 'Page load time for user: ' + page_load_time + 'ms' );
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
	$( '#speed' ).html( 'Detected bandwidth is: '+ mbps + 'Mbps' );
}
		 
$( document ).ready( function() {
	getos();
	getbrowser();
	getspeed();
	getloadtime();
});

