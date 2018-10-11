# Ytdl2RSS

Transform any playlist understood by [YoutubeDL](https://github.com/rg3/youtube-dl) into a
iTunes-Compatible podcast XML.

## params
* `--file` Output file, will be overridden if exists
* `--url` URL of the podcast, eg. https://www.youtube.com/user/lukxde/videos
* `--min-duration` (optional) minimum duration of an entry to be considered part of the feed 

## Usage Example
```
python ytdl2rss --file ../html/podcasts/heute-show.xml --url https://www.zdf.de/comedy/heute-show --min-duration 600
```

## installation
```
pip install -r requirements.txt
``` 