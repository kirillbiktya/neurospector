import subprocess
from queue import Empty, Queue
from threading import Thread, current_thread


class FFmpegServer(Thread):
    def __init__(self, port: int, h: int, w: int, fps: int):
        self.im_h = h
        self.im_w = w
        self.im_bytesize = w * h * 3
        self.fps = fps
        self.port = port
        self.ffmpeg_process: subprocess.Popen | None = None
        self.stdout: subprocess.PIPE = None
        Thread.__init__(self)

    def run(self):
        vf = "fps={},scale={}x{}".format(self.fps, self.im_w, self.im_h)
        cmd = [
            "ffmpeg", "-f", "h264", "-listen", "1", "-y", "-an", "-sn", "-i", "tcp://0.0.0.0:" + str(self.port),
            "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-vf", vf, "-f", "image2pipe", "-"
        ]
        self.ffmpeg_process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            bufsize=self.im_bytesize * 10
        )
        self.stdout = self.ffmpeg_process.stdout
        self.ffmpeg_process.wait()


class FFmpegFrameEnqueuer(Thread):
    def __init__(self, server_instance: FFmpegServer, frame_queue: Queue):
        self.server_instance = server_instance
        self.frame_queue = frame_queue
        Thread.__init__(self)

    def _is_server_instance_alive(self):
        if self.server_instance.ffmpeg_process.poll() is not None:
            if self.server_instance.ffmpeg_process.poll() >= 0:
                return False
        else:
            return True

    def run(self):
        while current_thread().is_alive():
            im0 = b''
            while len(im0) < self.server_instance.im_bytesize:
                if not self._is_server_instance_alive():
                    break

                try:
                    buflen = self.server_instance.im_bytesize - len(im0)
                    im0 += self.server_instance.ffmpeg_process.stdout.read(buflen)
                except TypeError:
                    continue

            if len(im0) == self.server_instance.im_bytesize:
                self.frame_queue.put(im0)

            if not self._is_server_instance_alive() and len(im0) == 0:
                self.frame_queue.put("STOPP")
                break


def frame_generator(frame_queue: Queue):
    while True:
        try:
            x = frame_queue.get(False)
            if x is None:
                continue
            if x == "STOPP":
                break
            yield x
        except Empty:
            pass
