# TumblrLikesDownloader
This python script downloads all the photos and videos liked of your tumblr account. I refer to https://github.com/KellyReddington/TumblrLikesDownloader and https://gist.github.com/jeffaudi/89bba20e839d99e4afab .

Steps:

1. You need to register your app on [Tumblr](https://www.tumblr.com/oauth/register). You can leave most all the text fields blank. Don't get confused about the 'Default Callback URL', just put in the URL for your tumblr blog.

2. Go to the [Tumblr API console](https://www.tumblr.com/oauth/apps) and get Consumer Key, Consumer Secret, Token and Token Secret. It's all pretty self explanatory here. You simply copy and paste the keys/tokens from Tumblr into the tumblr_keys.py file located in the same folder as this README file. For more info, see below.

3. Edit file tumblr_keys.py and save in your keys.

4. Run
```
python download.py
```
