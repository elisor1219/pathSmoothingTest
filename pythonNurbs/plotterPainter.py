import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

class plotterPainter:

    _currentFigure = np.random.randint(100, 100000)
    _axis = []
    _grid = True
    _controlPoints = []
    _fontSizes = {'title': 20, 'label': 15}

    #TODO: Not the most elegent solution, but it works.
    _clickAndReleasePos = np.zeros((2,2))


    def __init__(self, axis: list):
        self._axis = axis
        self._initFigure()

    def _initFigure(self):
        plt.figure(self._currentFigure)
        plt.axis(self._axis)
        plt.grid(True)

    def givePoints(self):
        controlPoints = plt.ginput(-1, -1)
        self._controlPoints = np.array(controlPoints)
        return self._controlPoints

    def plotCurve(self, curvePoints: np.ndarray, degree: int, typOfCurve: str):
        self._initFigure()
        controlPoints = self._controlPoints

        labelPlt1 = 'Control points'
        labelPlt2 = 'Curve point of degree ' + str(degree)
        plt.plot(controlPoints[:,0], controlPoints[:,1], 'o--', label=labelPlt1)
        plt.plot(curvePoints[:,0], curvePoints[:,1], label=labelPlt2)
        plt.legend(prop={'size': self._fontSizes['label']})
        title = typOfCurve + ' curve'
        plt.title(title, fontsize=self._fontSizes['title'])
        #TODO: Maybe disconnect the mouse events?
        plt.connect('button_press_event', self.on_click)
        #TODO: Currently a bugg where the on_release is called twice.
        #      You can hold the left mouse button and then press Enter to not
        #      go into the press_event.
        plt.connect('button_release_event', self.on_release)
        plt.show()


    def on_click(self, event):
        if event.button is MouseButton.LEFT:
            xPos, yPos = event.xdata, event.ydata
            #If xPos and yPos are not None, then the click was inside the axes.
            if xPos != None or yPos != None:
                print('Left mouse button pressed at', event.xdata, event.ydata)
                self._clickAndReleasePos[0,0] = xPos
                self._clickAndReleasePos[0,1] = yPos


    def on_release(self, event):
        if event.button is MouseButton.LEFT:
            xPos, yPos = event.xdata, event.ydata
            #If xPos and yPos are not None, then the click was inside the axes.
            if xPos != None or yPos != None:
                print('Left mouse button released at', event.xdata, event.ydata)
                #TODO: Close the figure and return the x position.
                self._clickAndReleasePos[1,0] = xPos
                self._clickAndReleasePos[1,1] = yPos
                plt.close(self._currentFigure)
        


    def on_move(self, event):
        if event.inaxes:
            print(f'data coords {event.xdata} {event.ydata},',
                f'pixel coords {event.x} {event.y}')

    # - - - - - Getters - - - - -
    def getClickAndReleasePos(self):
        return self._clickAndReleasePos

    # - - - - - Setters - - - - -
    def setFontSizes(self, fontSizes: dict):
        self._fontSizes = fontSizes
