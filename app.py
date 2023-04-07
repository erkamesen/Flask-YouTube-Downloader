from flask import Flask, render_template, request, send_file, flash, abort
from datetime import datetime
from pytube import YouTube
from pytube.exceptions import RegexMatchError, PytubeError, VideoPrivate, LiveStreamError
from io import BytesIO
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

app.config.from_pyfile("config.py")


def download_video(link, req_type):
    buffer = BytesIO()
    url = YouTube(link)
    url.check_availability()
    title = url.title
    if req_type == "video":
        video = url.streams.get_highest_resolution()
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{title}.mp4", mimetype="video/mp4")
    elif req_type == "audio":
        audio = url.streams.get_audio_only()
        audio.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{title}.mp3", mimetype="audio/mp3")
    else:
        return abort(404)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        link = request.form.get("url")
        req_type = request.form.get("flexRadioDefault")
        try:
            buffer = BytesIO()
            url = YouTube(link)
            url.check_availability()
            title = url.title
            if req_type == "video":
                video = url.streams.get_highest_resolution()
                video.stream_to_buffer(buffer)
                buffer.seek(0)
                return send_file(buffer, as_attachment=True, download_name=f"{title}.mp4", mimetype="video/mp4")
            elif req_type == "audio":
                audio = url.streams.get_audio_only()
                audio.stream_to_buffer(buffer)
                buffer.seek(0)
                return send_file(buffer, as_attachment=True, download_name=f"{title}.mp3", mimetype="audio/mp3")
            else:
                return abort(404)
            
        except RegexMatchError:
            flash("Invalid URL")
            return render_template("index.html")
        except PytubeError:
            flash("Something is broken. Please try again later.")
            return render_template("index.html")
        except VideoPrivate:
            flash("This video is private")
            return render_template("index.html")
        except LiveStreamError:
            flash("This is a live video!!")
            return render_template("index.html")
    else:
        return render_template('index.html')


@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        link = request.form.get("url")
        buffer = BytesIO()
        url = YouTube(link)
        url.check_availability()
        video = url.streams.get_highest_resolution()
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="deneme.mp4", mimetype="video/mp4")
    else:
        return render_template("download.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=True)
