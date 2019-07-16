import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# PreAlignTracker
#

class PreAlignTracker(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Pre Align Tracker" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["Samuel C.P. Newhook (Sunnybrook Research Institute)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This module prealigns the segmented tracker from the optical scan with the loaded model file. This is run before surface registration of the tracker scan and tracker model.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
Todo: Put acknowledgements here.
""" # Todo: replace with organization, grant and thanks.

#
# PreAlignTrackerWidget
#

class PreAlignTrackerWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    #
    # Select models for prealignment
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Select Models"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
    # Select segmented optical scan of tracker
    #
    self.optical_tracker_model_selector = slicer.qMRMLNodeComboBox()
    self.optical_tracker_model_selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.optical_tracker_model_selector.selectNodeUponCreation = True
    self.optical_tracker_model_selector.addEnabled = False
    self.optical_tracker_model_selector.removeEnabled = False
    self.optical_tracker_model_selector.noneEnabled = False
    self.optical_tracker_model_selector.showHidden = False
    self.optical_tracker_model_selector.showChildNodeTypes = False
    self.optical_tracker_model_selector.setMRMLScene(slicer.mrmlScene)
    self.optical_tracker_model_selector.setToolTip("Choose the Optical Image of the Segmented Tracker")
    parametersFormLayout.addRow("Optical Image of Tracker: ", self.optical_tracker_model_selector)

    #
    # Select vtk model of tracker
    #
    self.template_tracker_model_selector = slicer.qMRMLNodeComboBox()
    self.template_tracker_model_selector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.template_tracker_model_selector.selectNodeUponCreation = True
    self.template_tracker_model_selector.addEnabled = True
    self.template_tracker_model_selector.removeEnabled = True
    self.template_tracker_model_selector.noneEnabled = True
    self.template_tracker_model_selector.showHidden = False
    self.template_tracker_model_selector.showChildNodeTypes = False
    self.template_tracker_model_selector.setMRMLScene(slicer.mrmlScene)
    self.template_tracker_model_selector.setToolTip("Choose the template Model of the Tracker.")
    parametersFormLayout.addRow("Template Model of the Tracker: ", self.template_tracker_model_selector)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.optical_tracker_model_selector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.template_tracker_model_selector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.optical_tracker_model_selector.currentNode() and self.template_tracker_model_selector.currentNode()

  def onApplyButton(self):
    logic = PreAlignTrackerLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    imageThreshold = self.imageThresholdSliderWidget.value
    logic.run(self.optical_tracker_model_selector.currentNode(), self.template_tracker_model_selector.currentNode(), imageThreshold, enableScreenshotsFlag)

#
# PreAlignTrackerLogic
#

class PreAlignTrackerLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('PreAlignTrackerTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True


class PreAlignTrackerTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_PreAlignTracker1()

  def test_PreAlignTracker1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = PreAlignTrackerLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
