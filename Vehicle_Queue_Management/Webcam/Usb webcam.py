from subprocess import call
from datetime import datetime


def capture():
    call(["fswebcam", "-d","/dev/video0", "-r", "640x480", "--no-banner", "./output.jpg"] )

capture()
