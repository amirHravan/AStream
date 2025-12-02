#!/bin/bash
set -e

# Go to dist/server
cd "$(dirname "$0")"

mkdir -p media/video
mkdir -p media/mpd/short
mkdir -p media/mpd/long

cd media/video

# Download source video (10s) - 1080p
if [ ! -f source_10s.mp4 ]; then
    echo "Downloading source video (1080p)..."
    # Using 10MB version for better quality source
    wget -q https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/1080/Big_Buck_Bunny_1080_10s_10MB.mp4 -O source_10s.mp4
fi

# Loop to 600s (10 min) for 100 long segments
if [ ! -f source.mp4 ]; then
    echo "Creating 600s video..."
    ffmpeg -stream_loop 59 -i source_10s.mp4 -c copy -y source.mp4
fi

# Create representations
echo "Transcoding representations..."
# Low - 1Mbps
ffmpeg -i source.mp4 -c:v libx264 -b:v 1000k -s 854x480 -x264-params "keyint=60:min-keyint=60:scenecut=0" -flags +cgop -c:a aac -b:a 128k -y video_1000k.mp4
# Medium - 2Mbps
ffmpeg -i source.mp4 -c:v libx264 -b:v 2000k -s 1280x720 -x264-params "keyint=60:min-keyint=60:scenecut=0" -flags +cgop -c:a aac -b:a 128k -y video_2000k.mp4
# High - 6Mbps
ffmpeg -i source.mp4 -c:v libx264 -b:v 6000k -s 1920x1080 -x264-params "keyint=60:min-keyint=60:scenecut=0" -flags +cgop -c:a aac -b:a 128k -y video_6000k.mp4

cd ../..

# Generate Short Segments (2s)
echo "Generating Short Segments MPD..."
ffmpeg -i media/video/video_1000k.mp4 -i media/video/video_2000k.mp4 -i media/video/video_6000k.mp4 \
    -map 0 -map 1 -map 2 \
    -c copy \
    -use_timeline 0 -use_template 1 \
    -seg_duration 2 \
    -adaptation_sets "id=0,streams=v" \
    -f dash \
    media/mpd/short/manifest.mpd

# Generate Long Segments (6s)
echo "Generating Long Segments MPD..."
ffmpeg -i media/video/video_1000k.mp4 -i media/video/video_2000k.mp4 -i media/video/video_6000k.mp4 \
    -map 0 -map 1 -map 2 \
    -c copy \
    -use_timeline 0 -use_template 1 \
    -seg_duration 6 \
    -adaptation_sets "id=0,streams=v" \
    -f dash \
    media/mpd/long/manifest.mpd

echo "Content setup complete."
