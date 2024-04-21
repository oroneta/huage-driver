#ffplay 播放，有时延
python3 driver2.py | ffplay -
 
#low latency play
python3 driver2.py | ffmpeg -threads 1 -re -fflags nobuffer  -f mjpeg -i - -pix_fmt yuv420p -f sdl -
 
python3 wificam_udp_cam_stop.py 
 
#Gstreamer也可以播放，
python3 driver2.py  | gst-launch-1.0  filesrc location=/dev/stdin ! queue ! jpegdec ! autovideosink
 