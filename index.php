<!DOCTYPE html>

<html lang="en" data-cast-api-enabled="true">

<?PHP

	function getVideoId($gotLink) {
		
		preg_match('%\?v=[a-zA-Z0-9_\-]+%',$gotLink,$inputVideoId);

		$inputVideoId = preg_replace('%\?v=%','',$inputVideoId[0]);
		
		return $inputVideoId;
		
	}

// get the source code of the youtube page to be bennytized
	function getYoutubeSource($videoId) {
		
		$youtubeUrl = sprintf("www.youtube.com/watch?v=%s", $videoId);
		
//		echo $youtubeUrl;
		
		$handle = curl_init($youtubeUrl);	
			
		curl_setopt($handle, CURLOPT_RETURNTRANSFER, TRUE);
		
		$response = curl_exec($handle);
			
		$httpCode = curl_getinfo($handle, CURLINFO_HTTP_CODE);
			
		curl_close($handle);
			
		if ($httpCode == 200) {

			$source = htmlspecialchars($response);
			
			return $source;
			
		}
		
	}
	
	function getMutedPlayer($videoId) {
		
		$embedVideoString = htmlspecialchars(file_get_contents('./morebenny.html'));
		
		$embedVideoString = preg_replace('%VIDEO_ID_HERE%',$videoId,$embedVideoString);
		
//		echo $embedVideoString;		
	
		return $embedVideoString;
		
	}
	
	function bennytizeSource($source, $embedVideoString) {
		
		$regExps = array();
// stock player			
		$regExps[0] = '%&lt;div id=&quot;player-api&quot; class=&quot;player-width player-height off-screen-target  player-api&quot;&gt;&lt;/div&gt;%';

//		$regExps[0] = '%&lt;div id=&quot;player-api&quot;.+ytplayer\.config\.loaded = true\n( )+}\)\(\);\n( )+&lt;/script&gt;%s';
// end body tag	and html tag			
		$regExps[1] = '%&lt;/body&gt;&lt;/html&gt;%';
// end of the css link
		$regExps[2] = '%\.css&quot; data-loaded=&quot;true&quot;&gt;%';
// youtube doctype and html tags
		$regExps[3] = '%&lt;\!DOCTYPE html&gt;&lt;html lang=&quot;en&quot; data-cast-api-enabled=&quot;true&quot;&gt;%';


		$replacements = array();
// muted player				
		$replacements[0] = $embedVideoString;
// benny, some jquery css and link modifications at the end

//   $(\'#player\').css(\'margin-left\',\'400px\');
//   $(\'#watch7-container\').position().left;

		$replacements[1] = '&lt;script&gt;
$( document ).ready(function() {
   $(\'#player.watch-small\').css(\'min-width\',\'640px\');
   var offset = $(\'#watch7-container\').position().left;
   $(\'#player\').css(\'margin-left\',offset);
   $(\'#watch7-main\').css(\'min-width\',\'640px\');
});
&lt;/script&gt;
&lt;object width=&quot;420&quot; height=&quot;315&quot;&gt;&lt;param name=&quot;movie&quot; value=&quot;//www.youtube.com/v/MK6TXMsvgQg?hl=en_US&amp;version=3&quot;&gt;&lt;/param&gt;&lt;param name=&quot;allowFullScreen&quot; value=&quot;true&quot;&gt;&lt;/param&gt;&lt;param name=&quot;allowscriptaccess&quot; value=&quot;always&quot;&gt;&lt;/param&gt;&lt;embed src=&quot;//www.youtube.com/v/MK6TXMsvgQg?hl=en_US&amp;version=3;autoplay=1&quot; type=&quot;application/x-shockwave-flash&quot; width=&quot;420&quot; height=&quot;315&quot; allowscriptaccess=&quot;always&quot; allowfullscreen=&quot;true&quot;&gt;&lt;/embed&gt;&lt;/object&gt;
&lt;script&gt;
$("a").each(function() {
   this.href=&quot;/&quot;;
})&lt;/script&gt;';

// include jquery so we can do the above modifications to css
		$replacements[2] = '.css&quot; data-loaded=&quot;true&quot;&gt;
  &lt;script src=&quot;http://code.jquery.com/jquery-2.1.0.min.js&quot;&gt;&lt;/script&gt;';
// remove
		$replacements[3] = '';
				
		$bennytizedSource = preg_replace($regExps,$replacements,$source); 	
		
		$bennytizedSource = htmlspecialchars_decode($bennytizedSource);	
		
		return $bennytizedSource;
		
	}

	function bennytize($videoId) {
		
// get the youtube source for the target videoId	
		$source = getYoutubeSource($videoId);

//get the code for a muted video and swap in the target videoId		
		$embedVideoString = getMutedPlayer($videoId);

//modify the youtube source code 
		$bennytizedSource = bennytizeSource($source,$embedVideoString);
		
		return $bennytizedSource;
		
		
	}
	
	function bitlytize($videoId) {
		
		$bennyLink = sprintf("http://www.bennytize.me/?v=%s", $videoId);
		
		$bitlyToken = "4108de02178b34ed1c1f0fc207c020dc06b8aeed";
		
		$bitlyResponse = json_decode(file_get_contents("https://api-ssl.bitly.com/v3/shorten?access_token={$bitlyToken}&longUrl={$bennyLink}&format=json"));
		
		$bitlyLink = $bitlyResponse->data->url;
		
		return $bitlyLink;
		
	}


// get the current page url. used to tell if we should render a benny page, get a benny link, or give a benny link
// stackoverflow.com/questions/5598480/php-parse-current-url
	function curPageURL() {
		
		$pageURL = 'http';
		
		if ($_SERVER["HTTPS"] == "on") {$pageURL .= "s";}
		
			$pageURL .= "://";
		
		if ($_SERVER["SERVER_PORT"] != "80") {
		
			$pageURL .= $_SERVER["SERVER_NAME"].":".$_SERVER["SERVER_PORT"].$_SERVER["REQUEST_URI"];
		
		} else {
		
			$pageURL .= $_SERVER["SERVER_NAME"].$_SERVER["REQUEST_URI"];
		
		}
		
		return $pageURL;
	}



	$bennyHome = file_get_contents('./bennyhome.html');

	if (isset($_POST['gotLink'])) {
	
		if (preg_match('%www\.youtube\.com/watch\?v=[a-zA-Z0-9_]+%',$_POST['gotLink'])) {
			
			$videoId = getVideoId($_POST['gotLink']);
			
			$bitlyLink = bitlytize($videoId);

			$bennyHome = preg_replace('%VALUE = \"\"%',"VALUE = \"".$bitlyLink."\"", $bennyHome);
			
			$bennyHome = preg_replace('%TEXT_GOES_HERE%',"<h3>Here's your Bennylink:</h3><br>", $bennyHome);

			echo $bennyHome;
			
			}
		
		else {
			
			$bennyHome = preg_replace('%TEXT_GOES_HERE%',"<h3>That URL was no good. Paste a YouTube video URL below!</h3>", $bennyHome);
			
			echo $bennyHome;
			
		}
	}
		
	else {
// check if the entred URL is a bennylink and if so render a bennypage
		$curUrl = curPageURL();
		
		$videoId = getVideoId($curUrl);
		
		if ($videoId) {
			
			$bennytizedSource = bennytize($videoId);
			
			echo $bennytizedSource;
		}

		else {
		
			$bennyHome = preg_replace('%TEXT_GOES_HERE%',"<h3>Paste a YouTube video URL below!</h3>", $bennyHome);
			
			echo $bennyHome;
		}
	}
?>

</html>
