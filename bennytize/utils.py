


import re
import requests

from bennytize import app

def get_bennylink(youtube_url):
    """
        create a bitly link for the bennytized page
    """

    video_id = re.search('\?v=[a-zA-Z0-9_\-]+', youtube_url).group()

    url = 'http://{}/{}'.format(app.config['DOMAIN_NAME'],video_id[3:])

    r = requests.get(
        'https://api-ssl.bitly.com/v3/shorten?access_token={}&longUrl={}&format=json'
            .format(app.config['BITLY_API_TOKEN'],url)
    )

    print r.json()

    return r.json()['data']['url']

def bennytize(video_id):

    source = requests.get('https://youtube.com/watch?v={}'.format(video_id)).content
    source = source.decode('ascii', errors='ignore')
    source = add_benny(source)
    source = add_jquery(source)
    source = add_muted_player(source, video_id)
    source = change_links(source)

    return source

def add_benny(source):
    """
        put the benny video at the end of the page
    """

    target = '</body></html>'
    replacement = '''
<iframe id="ytplayer" type="text/html" width="640" height="390"
  src="http://www.youtube.com/embed/MK6TXMsvgQg?autoplay=1"
  frameborder="0"></iframe>
</body></html>'''

    return source.replace(target, replacement)

def add_jquery(source):
    """
        add jquery in the head
    """
    target = '<head>'
    replacement = '<head><script src="http://code.jquery.com/jquery-2.1.0.min.js"></script>'
    source = source.replace(target, replacement)

    return source.replace(target, replacement)

def add_muted_player(source, video_id):
    """
        replace the original youtube player with a muted one
    """

    original_player = '<div id="player-api" class="player-width player-height off-screen-target player-api" tabIndex="-1"></div>'
    muted_player = '''
<!-- 1. The <iframe> (and video player) will replace this <div> tag. -->
    <div id="mutedplayer" class="player-api player-width player-height"></div>

    <script>
      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {
        player = new YT.Player('mutedplayer', {
          height: '390',
          width: '640',
          videoId: 'VIDEO_ID_HERE',
          events: {
            'onReady': onPlayerReady,
          }
        });
      }

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {
        event.target.mute();
        event.target.playVideo();
      }
</script>
'''
    source = source.replace(original_player,'')
    target = '<div class="player-api player-width player-height">'

    return source.replace(target, target+muted_player.replace('VIDEO_ID_HERE', video_id))

def change_links(source):
    """
        chang all links to go to bennytize homepage
    """

    target = '</body></html>'

    replacement = '''
<script>
$("a").each(function() {
   this.href="/";
})</script>
'''
    return source.replace(target, replacement)