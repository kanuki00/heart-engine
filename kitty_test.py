import sys
from base64 import standard_b64encode as b64e

start = b"\033_G"
# a = action to perform (T means "transmit data and display image")
# f = pixel format (24 means 24-bit RGB),
# s = image width,
# v = image height
control = b"a=T,f=24,s=100,v=100;"
arr = [bytes.fromhex("ff0000")]*10000
payload = b64e(b"".join(arr))
end = b"\003\\"
output = [start, control, payload, end]

sys.stdout.buffer.write(b"".join(output))
sys.stdout.flush()
