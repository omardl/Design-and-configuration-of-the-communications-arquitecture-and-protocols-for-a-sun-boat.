import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)

pipeline = Gst.Pipeline.new("rtsp-server")

rtp = Gst.ElementFactory.make("rtph264depay", "rtp-depayloader")


decoder = Gst.ElementFactory.make("avdec_h264", "h264-decoder")

sink = Gst.ElementFactory.make("fakesink", "sink")

server = Gst.ElementFactory.make("rtspserver", "rtsp-server")

pipeline.add(rtp)
pipeline.add(decoder)
pipeline.add(sink)
pipeline.add(server)

rtp.link(decoder)
decoder.link(sink)

server.set_property("address", "192.168.0.15")
server.set_property("service", "1234")

pipeline.set_state(Gst.State.PLAYING)

Gst.main()