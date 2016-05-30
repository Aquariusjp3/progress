import os

import logging

from PySide import QtCore
from PySide import QtGui


class ProgressHandler(logging.Handler):
	''' A class for using log records to step the progress window '''

	def __init__(self, window):
		super(ProgressHandler, self).__init__(level=0)

		self.window = window

	def emit(self, record):
		''' Override to call the step method on the progress window instead
		of actually emitting the record.
		'''
		self.window.step(record)


class ProgressBar(object):
	''' Progress bar context class '''

	def __init__(self, title=None, maximum=100):
		# Create the progress bar window instance
		self.window = ProgressBarWindow(title, estimated_steps)

		# Get the root logger, we will use this to attach the handler to, to
		# make sure we get all logged events during the progress bar run.
		self.root = logging.getLogger()

	def __enter__(self):
		# Create the handler and add it to the root logger
		self.handler = ProgressHandler(self.window)
		self.root.addHandler(self.handler)

	def __exit__(self, type, value, traceback):
		# Remove the handler and cleanup
		self.logger.removeHandler(self.handler)
		self.window.close()


class ProgressBarWindow(QtGui.QWidget):
	''' A simple progress bar window '''

	def __init__(self, title=None, maximum=100):
		super(ProgressBarWindow, self).__init__()

		self.setWindowTitle(title)

		# Create the UI
		self.layout = QtGui.QVBoxLayout()
		self.setLayout(self.layout)

		self.label = QtGui.QLabel()
		self.label.setMinimumHeight(30)

		self.separator = QtGui.QFrame()
		self.separator.setFrameStyle(QtGui.QFrame.VLine)
		self.separator.setFrameShadow(QtGui.QFrame.Sunken)

		self.progressBar = QtGui.QProgressBar()
		self.progressBar.setMaximum(maximum)
		self.progressBar.setMinimumHeight(50)
		self.progressBar.setMinimumWidth(500)

		self.layout.addWidget(self.label)
		self.layout.addWidget(self.separator)
		self.layout.addWidget(self.progressBar)

		self.show()

	def step(self, record):
		''' Step the progress bar and show the message '''
		value = self.progressBar.value() + 1 # New value

		# If the value were to go over the maximum of the progress bar,
		# instead reset it back to 0 and continue.
		if value > self.progressBar.maximum():
			value = 1

		self.progressBar.setValue(value)

		# Show the message in the label
		self.label.setText(record.getMessage())
		