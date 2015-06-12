#! /usr/bin/env python3
import tkinter as tk
import time

class StopWatch(tk.Frame):

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.grid_rowconfigure(1, weight=1)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = tk.StringVar(self, '0.000000')
        self.e = 0
        self.m = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
        
    def makeWidgets(self):                         
        """ Make the time label. """
        self._frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self._frame.pack(fill=tk.BOTH, expand=1)
        
        self.pack(fill=tk.BOTH, expand=1)

        self._frame._label1 = tk.Label(self._frame, text='----File Name----')
        self._frame._label1.pack(fill=tk.X, expand=tk.NO, pady=1, padx=2)
        self._frame._entry = tk.Entry(self._frame)
        self._frame._entry.pack(pady=2, padx=2)

        self._frame._label0 = tk.Label(self._frame, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        self._frame._label0.pack(fill=tk.X, expand=tk.NO, pady=3, padx=2)

        self._frame._label2 = tk.Label(self._frame, text='----Laps----')
        self._frame._label2.pack(fill=tk.X, expand=tk.NO, pady=4, padx=2)

        self._frame._scrollbar = tk.Scrollbar(self._frame, orient=tk.VERTICAL)
        self._frame._listbox = tk.Listbox(self._frame, selectmode=tk.EXTENDED, height = 10, yscrollcommand=self._frame._scrollbar.set)
        self._frame._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, pady=5, padx=2)
        self._frame._scrollbar.config(command=self._frame._listbox.yview)
        self._frame._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def _stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def _reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.laps = []   
        self.lapmod2 = self._elapsedtime
        self._setTime(self._elapsedtime)
        self._frame._listbox.delete(0, tk.END)

    def _lap(self):
        '''Makes a lap, only if started'''
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self._frame._listbox.insert(tk.END, self.laps[-1])
            self._frame._listbox.yview_moveto(1)
            self.lapmod2 = self._elapsedtime
       
    def _saveCSV(self):
        '''Pega nome do cronometro e cria arquivo para guardar as laps'''
        filename = str(self._frame._entry.get()) + ' - '
        with open(filename + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))

    @classmethod
    def main(cls):
        root = tk.Tk()
        root.title('Stop Watch')
        root.wm_attributes("-topmost", 1)      #always on top - might do a button for it
        widget = StopWatch(root)
        widget.pack(side=tk.TOP)

        widget._button = tk.Button(widget, text='Start', command=widget.Start).pack(side=tk.LEFT, pady=5, padx=5)
        widget._button = tk.Button(widget, text='Lap', command=widget._lap).pack(side=tk.LEFT)
        widget._button = tk.Button(widget, text='Stop', command=widget._stop).pack(side=tk.LEFT)
        widget._button = tk.Button(widget, text='Reset', command=widget._reset).pack(side=tk.LEFT)
        widget._button = tk.Button(widget, text='Save', command=widget._saveCSV).pack(side=tk.LEFT)
        widget._quitbutton = tk.Button(widget, text='Quit', command=widget.quit).pack(side=tk.LEFT)
        
        root.mainloop()

if __name__ == '__main__':
    StopWatch.main()
