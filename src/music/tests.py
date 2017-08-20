import random
import string

import factory
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

from music.models import Album, Song
from music.views import AlbumListView


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "Agent %03d" % n)
    email = factory.LazyAttributeSequence(lambda o, n: f'{o.username}{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password')


class AlbumFactory(factory.DjangoModelFactory):
    class Meta:
        model = Album

    artist = 'MyArtist'
    album_title = 'MyAlbumTitle'
    genre = 'MyGenre'


class SongFactory(factory.DjangoModelFactory):
    class Meta:
        model = Song

    album = factory.SubFactory(AlbumFactory)
    file_type = 'MyFileType'
    song_title = 'MySongTitle'
    is_favorite = 'False'


class AlbumTests(TestCase):
    def test_str(self):
        album = AlbumFactory()
        self.assertEqual(str(album), 'MyAlbumTitle . MyArtist')


class SongTests(TestCase):
    def test_str(self):
        s = SongFactory()
        self.assertEqual(str(s), 'MySongTitle')


class AlbumListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory(password=random_string_generator())

    def test_no_albums_in_context(self):
        request = self.factory.get('/')
        request.user = self.user
        response = AlbumListView.as_view()(request)
        self.assertEquals(list(response.context_data['object_list']), [],)

    def test_albums_in_context(self):
        request = self.factory.get('/')
        album = AlbumFactory()
        request.user = self.user
        response = AlbumListView.as_view()(request)
        self.assertEquals(list(response.context_data['object_list']), [album],)


class CreatePostIntegrationTest(LiveServerTestCase):
    selenium = None

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        cls.password = random_string_generator()
        cls.user = UserFactory(password=cls.password)
        cls.client = Client()
        super(CreatePostIntegrationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(CreatePostIntegrationTest, cls).tearDownClass()

    def test_create_album(self):
        self.assertTrue(self.client.login(username=self.user.username, password=self.password))
        cookie = self.client.cookies[settings.SESSION_COOKIE_NAME]
        # Replace `localhost` to 127.0.0.1 due to the WinError 10054 according to the
        # https://stackoverflow.com/a/14491845/1360307
        self.selenium.get(f'{self.live_server_url}{reverse("music:album_create")}'.replace('localhost', '127.0.0.1'))
        if cookie:
            self.selenium.add_cookie({
                'name': settings.SESSION_COOKIE_NAME,
                'value': cookie.value,
                'secure': False,
                'path': '/'})
        self.selenium.refresh()  # need to update page for logged in user
        self.selenium.find_element_by_id('id_artist').send_keys('MyArtist')
        self.selenium.find_element_by_id('id_album_title').send_keys('MyAlbumTitle')
        self.selenium.find_element_by_id('id_genre').send_keys('MyGenre')
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()
        self.assertEqual(Album.objects.first().album_title, 'MyAlbumTitle')
