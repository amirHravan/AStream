#!/usr/bin/env python3
import time
import http.server
import sys
import os
from argparse import ArgumentParser
from collections import defaultdict
from list_directory_py3 import list_directory
import itertools

# Default values
DEFAULT_HOSTNAME = '127.0.0.1'
DEFAULT_PORT = 8006
DEFAULT_SLOW_RATE = 0.001

BLOCK_SIZE = 1024

# Values set by the option parser
PORT = DEFAULT_PORT
HOSTNAME = DEFAULT_HOSTNAME
HTTP_VERSION = "HTTP/1.1"
SLOW_RATE = DEFAULT_SLOW_RATE

HTML_PAGES = ['index.html', 'list.html', 'media/my_image.png']
# We need to update MPD_FILES to include our new files or just check extension
MPD_FILES = ['media/mpd/x4ukwHdACDw.mpd', "media/mpd/x4ukwHdACDw_filesize.mpd"]
HTML_404 = "404.html"

ACTIVE_DICT = defaultdict(dict)
SLOW_COUNT = 1000
DELAY_VALUES = dict()

def delay_decision():
    """ Module to decide if the segemnt is to be delayed or not"""
    for i in range(30):
        if i % 3 == 0:
            yield 0
        yield 1

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTPHandler to serve the DASH video"""

    def do_GET(self):
        """Function to handle the get message"""
        request = self.path.split('?')[0]
        if request.startswith('/'):
            request = request[1:]
        
        # connection_id = client IP, dirname of file
        connection_id = (self.client_address[0],
                         os.path.dirname(self.path))
        
        #check if the request is for the a directory
        if request.endswith('/') or os.path.isdir(request):
            if not request.endswith('/'):
                request += '/'
            dir_listing = list_directory(request)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            duration = dir_write(self.wfile, dir_listing)
        elif request in HTML_PAGES:
            print("Request HTML %s" % request)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            duration = normal_write(self.wfile, request)
        elif request.endswith('.mpd'):
            print("Request for MPD %s" % request)
            if os.path.exists(request):
                self.send_response(200)
                self.send_header("Content-type", "application/dash+xml")
                self.end_headers()
                duration, _ = normal_write(self.wfile, request)
                if connection_id in ACTIVE_DICT:
                    del (ACTIVE_DICT[connection_id])
            else:
                self.send_error(404)
        elif request.split('.')[-1] in ['m4f', 'mp4', 'm4s', 'm4v']:
            print("Request for DASH Media %s" % request)
            if os.path.exists(request):
                if connection_id not in ACTIVE_DICT:
                    ACTIVE_DICT[connection_id] = {
                        'file_list': [os.path.basename(request)],
                        'iter': itertools.cycle(delay_decision())}
                else:
                    ACTIVE_DICT[connection_id]['file_list'].append(
                        os.path.basename(request))

                self.send_response(200)
                # self.send_header("Content-type", "video/mp4") # Optional
                self.end_headers()
                duration, file_size = normal_write(self.wfile, request)
                print('Normal: Request took {} seconds for size of {}'.format(duration, file_size))
            else:
                self.send_error(404)
        else:
            self.send_error(404)
            return

def normal_write(output, request):
    """Function to write the video onto output stream"""
    start_time = time.time()
    data_len = 0
    try:
        with open(request, 'rb') as request_file:
            while True:
                data = request_file.read(BLOCK_SIZE)
                if not data:
                    break
                output.write(data)
                data_len += len(data)
            output.flush()
    except IOError:
        pass
    now = time.time()
    return now - start_time, data_len

def dir_write(output, data):
    """Function to write the video onto output stream"""
    start_time = time.time()
    output.write(data.read())
    now = time.time()
    output.flush()
    return now - start_time

def start_server():
    """ Module to start the server"""
    http_server = http.server.HTTPServer((HOSTNAME, PORT),
                                            MyHTTPRequestHandler)
    print(" ".join(("Listening on ", HOSTNAME, " at Port ",
                    str(PORT), " - press ctrl-c to stop")))
    http_server.serve_forever()

def create_arguments(parser):
    """ Adding arguments to the parser"""
    parser.add_argument('-p', '--PORT', type=int,
                        help=("Port Number to run the server. Default = %d" % DEFAULT_PORT), default=DEFAULT_PORT)
    parser.add_argument('-s', '--HOSTNAME', help=("Hostname of the server. Default = %s"
                                                  % DEFAULT_HOSTNAME), default=DEFAULT_HOSTNAME)
    parser.add_argument('-d', '--SLOW_RATE', type=float, help=(
        "Delay value for the server in msec. Default = %f" % DEFAULT_SLOW_RATE),
                        default=DEFAULT_SLOW_RATE)

def update_config(args):
    """ Module to update the config values with the a
    arguments """
    globals().update(vars(args))
    return

def main():
    """Program wrapper"""
    parser = ArgumentParser(description='Process server parameters')
    create_arguments(parser)
    args = parser.parse_args()
    update_config(args)
    start_server()

if __name__ == "__main__":
    sys.exit(main())
