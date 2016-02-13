



## azealia banks - 212
TEST_YOUTUBE_URL = 'https://www.youtube.com/watch?v=YdiggyoQhoc'

from bennytize import utils

def test_get_benny_link():

    bennylink = utils.get_bennylink(TEST_YOUTUBE_URL)

    print bennylink

    assert bennylink is not None

def test_get_bitly_link():

    video_id = utils.get_video_id(TEST_YOUTUBE_URL)

    bennylink = utils.get_bennylink(video_id)

    bitly_link = utils.get_bitly_link(bennylink)

    print bitly_link

    assert bitly_link is not None

def test_get_youtube_source():

    youtube_source = utils.get_youtube_source(TEST_YOUTUBE_URL)

    assert youtube_source is not None