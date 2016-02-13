


import re
import requests

from bennytize import app

def get_bennylink(youtube_url):

    video_id = re.search('\?v=[a-zA-Z0-9_\-]+', youtube_url).group()

    return 'http://bennytize.me/{}'.format(video_id)

def get_bitly_link(url):

    r = requests.get(
        'https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}&format=json'
            .format(app.config['BITLY_API_TOKEN'],url)
    )

    return r.json()['data']['url']

def bennytize(video_id):

    source = requests.get('https://youtube.com/watch?v={}'.format(video_id)).content

    source = add_jquery(source)

    source = add_css(source)

    source = add_muted_player(source, video_id)

    return source

def add_jquery(source):

    target = '</body></html>'

# <script>
# $( document ).ready(function() {
#    $('#player.watch-small').css('min-width','640px');
#    var offset = $('#watch7-container').position().left;
#    $('#player').css('margin-left',offset);
#    $('#watch7-main').css('min-width','640px');
# });
# </script>

    replacement = '''
<object width="1" height="1"><param name="movie" value="//www.youtube.com/v/MK6TXMsvgQg?hl=en_US&version=3"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="//www.youtube.com/v/MK6TXMsvgQg?hl=en_US&version=3;autoplay=1" type="application/x-shockwave-flash" width="420" height="315" allowscriptaccess="always" allowfullscreen="true"></embed></object>
<script>
$("a").each(function() {
   this.href="/";
})</script></body></html>'''

    return source.replace(target, replacement)

def add_css(source):

    target = '\.css" data-loaded="true">'

    replacement = '.css" data-loaded="true"><script src="http://code.jquery.com/jquery-2.1.0.min.js"></script>'

    return source.replace(target, replacement)

def add_muted_player(source, video_id):

    target = '<div id="player-api" class="player-width player-height off-screen-target player-api" tabIndex="-1"></div>'

    replacement ='''<!-- 1. The <div> tag will contain the <iframe> (and video player) -->
<div id="player"></div>
<script>      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');
      
      tag.src = "http://www.youtube.com/iframe_api";
      
      var firstScriptTag = document.getElementsByTagName('script')[0];
      
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('player', {
          height: '390',
          width: '640',
          playerVars: { 'autoplay': 1, 'controls': 1,'autohide':1,'wmode':'opaque' },
          videoId: 'VIDEO_ID_HERE',
          events: {
            'onReady': onPlayerReady}
        });  
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
        event.target.mute();
      }
</script>
'''

    return source.replace(target, replacement.replace('VIDEO_ID_HERE', video_id))
    
def replace_stock_player(source, video_id):

    stock_player_regexp = '<div id="player-api" class="player-width player-height off-screen-target  player-api"></div>'


