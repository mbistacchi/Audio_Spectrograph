# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 12:19:37 2019

@author: MSI Gaming
"""

import numpy as np
import pyaudio
import matplotlib.pyplot as plt


class SpectrumAnalyzer:
    
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 44100
    CHUNK = 4096
    N = CHUNK
    START = 0 
    # n.b. T_total =  N / Fs
    counter = 0

    def __init__(self):
        
        self.data = []
        self.pause = False
        
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format = self.FORMAT,
            channels = self.CHANNELS, 
            rate = self.RATE, 
            input = True,
            output = False,
            frames_per_buffer = self.CHUNK)
        
        self.init_graphs()
        # Main loop
        self.loop()

    def loop(self):
        try:
            while not self.pause :
                print("cycle:", self.counter)
                self.counter += 1
                
                self.data = self.audioinput()
                self.wave()
                self.fft()
                self.graphplot()

        except KeyboardInterrupt:
            self.pause = True
            print("End...")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.fromstring(ret, np.float32)
        return ret


    def wave(self):    
        self.x = self.data[self.START : self.START + self.N] # needed?

    def fft(self):
        self.X = np.abs(np.fft.rfft(self.data[self.START:self.START + self.N - 1]))    

        
    def init_graphs(self):
        
        # Both x axis definition
        self.t = np.arange(self.START, self.START + self.N) / self.RATE
        self.f = self.RATE * np.arange(self.N/2) / self.N 
        
        # initialize plot
        self.fig, (ax1, ax2) = plt.subplots(2, 1)
        self.linet, = ax1.plot(self.t, np.zeros(len(self.t)))
        self.linef, = ax2.plot(self.f, np.zeros(len(self.f)))
        
        # format axis
        ax1.set_xlabel("time [s]")
        ax1.set_ylabel("x(t)")
        ax2.set_xlabel("Freq [Hz]")
        ax2.set_ylabel("X(f)")
        
        # axis limits
        ax1.set_xlim(0, self.N / self.RATE)
        ax1.set_ylim(-2, 2)
        ax2.set_xlim(20, self.RATE / 2) # Nyquist
        ax2.set_ylim(0, 50)
        
        plt.show(block = False)

    def graphplot(self):            
        self.linet.set_ydata(self.x) # wave                    
        self.linef.set_ydata(self.X) # Spectrum

        #Pause
        #plt.pause(self.N / self.RATE)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == "__main__":
    spec = SpectrumAnalyzer()