import numpy as np
from gnuradio import gr
import time

class blk(gr.sync_block):
def __init__(self, filename="/home/Desktop/LICENTA/semnal_curent.txt"):
gr.sync_block.__init__(
self,
name="RSSI average to file",
in_sig=[np.complex64],
out_sig=[]
self.filename = filename
self.last_write = 0
self.offset_db =-25
self.nfft = 2048
self.rssi_smooth = None
self.alpha = 0.15
def work(self, input_items, output_items):
samples = input_items[0]

if len(samples) < self.nfft:
return len(samples)
x = samples[:self.nfft]
n = len(x)
spectrum = np.fft.fftshift(np.fft.fft(x)) / n
power_spectrum = np.abs(spectrum) ** 2
start = int(0.10 * n)
end = int(0.90 * n)
useful_band = power_spectrum[start:end]

power = np.mean(useful_band)

if power > 0:
rssi_db = 10 * np.log10(power) + self.offset_db
else:
rssi_db =-999.0

if self.rssi_smooth is None:
self.rssi_smooth = rssi_db
else:
self.rssi_smooth = self.alpha * rssi_db + (1- self.alpha) * self.rssi_smooth
now = time.time()

if now- self.last_write >= 1.0:
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
with open(self.filename, "w") as f:
f.write("{}, {:.2f}\n".format(timestamp, self.rssi_smooth))

self.last_write = now

return len(samples)