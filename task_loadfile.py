import csv
import PyQt4
import data
import task

class Task(task.Task):
    def __init__(self, name, mainWindow, parent = None):
        """
        Parameters
        name: name of the opened file.
        """
        super(Task, self).__init__(mainWindow, parent)
        self.name = name

    def run(self):
        """
        The code in this method is run in another thread.
        """
        # Load data
        reader = csv.reader(open(self.name))
        try:
            self.mainWindow.data.originalData.readFromCsvReader(reader, self.messageAdded.emit)
        except (StopIteration, csv.Error):
            PyQt4.QtGui.QMessageBox.critical(self, "Error while loading file",
                                       "Error occured when loading " + name)
            return

        self.mainWindow.data.maxPoints = data.Data.DEFAULT_USED_POINTS_COUNT
        self.messageAdded.emit("Copying %d points from loaded data..." % self.mainWindow.data.maxPoints)
        self.mainWindow.data.fileName = self.name # full path
        self.mainWindow.data.fileCreated = PyQt4.QtCore.QFileInfo(self.name).lastModified()
        self.mainWindow.data.copyFromOriginalData()
        self.messageAdded.emit("Computing absorbance...")
        self.mainWindow.data.guessFullLightVoltagePointerValue() # sets fullLightVoltage
        self.mainWindow.data.recalculateAbsorbances()
        self.messageAdded.emit("Setting fit absorbance pointers")
        self.mainWindow.data.guessFitAbsorbanceTimePointer()

    def postRun(self):
        """
        The code in this method is run in GUI thread.
        """
        # Refresh GUI
        self.mainWindow.scene.updateFromData(True)
        self.mainWindow.setLoadedFilePath(self.name)
        self.mainWindow.settings.onDataLoaded(self.mainWindow.data)
        # Update Recent files in the Main Menu
        self.mainWindow.menuBar().addRecentFile(self.name)