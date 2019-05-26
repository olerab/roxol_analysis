# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
import glob


all_paths_in = ['/Volumes/PVPLAB2/OLE/roxol/RESULTS/90deg_random/compressional/1perc/']
all_paths_out = ['/Volumes/PVPLAB2/OLE/roxol/RESULTS/plots/90deg_random/compressional/1perc/']

numResults = 75

if len(all_paths_in) != len(all_paths_out):
	print('ERROR! path list for input and output files needs to be same length')

for i in range(0,len(all_paths_in)):
	# get correct file name lists
	fpath_in= all_paths_in[i]
	
	vtuFiles = glob.glob(all_paths_in[i] + '*.vtu')
	vtkFiles = glob.glob(all_paths_in[i] + '*.vtk')
	
	# output files specs	
	fname_out = all_paths_out[i] + 'animations/simple_network/FN_result.png'
	



# ----------- DO NOT EDIT FROM HERE UNLESS YOU REALLY NEED TO AND KNOW WHAT YOU ARE DOING -----------
	
	paraview.simple._DisableFirstRenderCameraReset()
	ResetSession()
	
	
	# create a new 'XML Unstructured Grid Reader'
	simulatorResults_ = XMLUnstructuredGridReader(FileName=vtuFiles)
	simulatorResults_.CellArrayStatus = ['element_displacement_$vector_$createComponentsAsScalar', 'element_strain_3esd_$createComponentsAsScalar', 'element_stress_3esd_$createComponentsAsScalar', 'element_principalStress_$vector_$createComponentsAsScalar', 'element_heaviside_$scalar', 'element_radialStress_$scalar', 'element_tangentialStress_$scalar', 'element_shearStress_$scalar', 'element_radialDisplacement_$scalar', 'element_tangentialDisplacement_$scalar', 'element_S1S3Quotient_$scalar', 'element_3S1minusS3_$scalar', 'element_3S3minusS1_$scalar', 'element_principalStress2d_$createComponentsAsScalar', 'element_elasticShearEnergyDensity_$scalar', 'element_porePressure_$scalar', 'element_porePressureGradient_$vector_$createComponentsAsScalar', 'element_fluidVolumeFlow_$vector_$createComponentsAsScalar', 'element_lastPrincipalDirection_$vector', 'element_material_ids_$scalar']
	simulatorResults_.PointArrayStatus = ['node_displacement_$vector_$createComponentsAsScalar', 'node_strain_3esd_$createComponentsAsScalar', 'node_stress_3esd_$createComponentsAsScalar', 'node_radialDisplacement_$scalar', 'node_tangentialDisplacement_$scalar', 'node_cylindrical_stress_$createComponentsAsScalar', 'node_principalStrains_$createComponentsAsScalar', 'node_principalStress_$createComponentsAsScalar', 'node_totalDisplacement_$scalar', 'node_maximumShearStress_$scalar', 'node_totalElasticStrainEnergy_$scalar', 'node_volumetricStrainEnergy_$scalar', 'node_deviatoricStrainEnergy_$scalar', 'node_levelsets_phi_$createComponentsAsScalar', 'node_enrichment_$createComponentsAsScalar', 'node_porePressure_$scalar', 'node_porePressureGradient_$vector_$createComponentsAsScalar', 'node_fluidVolumeFlow_$vector_$createComponentsAsScalar', 'node_averageSubResultDeviation_$scalar', 'node_maximalSubResultDeviation_$scalar']
	
	# get animation scene
	animationScene1 = GetAnimationScene()
	
	# update animation scene based on data timesteps
	animationScene1.UpdateAnimationUsingDataTimeSteps()
	
	# create a new 'Legacy VTK Reader'
	simulatorResultsGeometry_ = LegacyVTKReader(FileNames=vtkFiles)
	
	# set active source
	SetActiveSource(simulatorResults_)
	
	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [1830, 1166]
	
	# show data in view
	simulatorResults_Display = Show(simulatorResults_, renderView1)
	
	# trace defaults for the display properties.
	simulatorResults_Display.Representation = 'Surface'
	simulatorResults_Display.ColorArrayName = [None, '']
	simulatorResults_Display.OSPRayScaleArray = 'node_averageSubResultDeviation_$scalar'
	simulatorResults_Display.OSPRayScaleFunction = 'PiecewiseFunction'
	simulatorResults_Display.SelectOrientationVectors = 'None'
	simulatorResults_Display.ScaleFactor = 0.05
	simulatorResults_Display.SelectScaleArray = 'None'
	simulatorResults_Display.GlyphType = 'Arrow'
	simulatorResults_Display.GlyphTableIndexArray = 'None'
	simulatorResults_Display.GaussianRadius = 0.0025
	simulatorResults_Display.SetScaleArray = ['POINTS', 'node_averageSubResultDeviation_$scalar']
	simulatorResults_Display.ScaleTransferFunction = 'PiecewiseFunction'
	simulatorResults_Display.OpacityArray = ['POINTS', 'node_averageSubResultDeviation_$scalar']
	simulatorResults_Display.OpacityTransferFunction = 'PiecewiseFunction'
	simulatorResults_Display.DataAxesGrid = 'GridAxesRepresentation'
	simulatorResults_Display.SelectionCellLabelFontFile = ''
	simulatorResults_Display.SelectionPointLabelFontFile = ''
	simulatorResults_Display.PolarAxes = 'PolarAxesRepresentation'
	simulatorResults_Display.ScalarOpacityUnitDistance = 0.013800087806205617
	
	# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
	simulatorResults_Display.DataAxesGrid.XTitleFontFile = ''
	simulatorResults_Display.DataAxesGrid.YTitleFontFile = ''
	simulatorResults_Display.DataAxesGrid.ZTitleFontFile = ''
	simulatorResults_Display.DataAxesGrid.XLabelFontFile = ''
	simulatorResults_Display.DataAxesGrid.YLabelFontFile = ''
	simulatorResults_Display.DataAxesGrid.ZLabelFontFile = ''
	
	# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
	simulatorResults_Display.PolarAxes.PolarAxisTitleFontFile = ''
	simulatorResults_Display.PolarAxes.PolarAxisLabelFontFile = ''
	simulatorResults_Display.PolarAxes.LastRadialAxisTextFontFile = ''
	simulatorResults_Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
	
	# reset view to fit data
	renderView1.ResetCamera()
	
	# set active source
	SetActiveSource(simulatorResultsGeometry_)
	
	# show data in view
	simulatorResultsGeometry_Display = Show(simulatorResultsGeometry_, renderView1)
	
	# get color transfer function/color map for 'fluidPressure'
	fluidPressureLUT = GetColorTransferFunction('fluidPressure')
	
	# trace defaults for the display properties.
	simulatorResultsGeometry_Display.Representation = 'Surface'
	simulatorResultsGeometry_Display.ColorArrayName = ['POINTS', 'fluidPressure']
	simulatorResultsGeometry_Display.LookupTable = fluidPressureLUT
	simulatorResultsGeometry_Display.OSPRayScaleArray = 'fluidPressure'
	simulatorResultsGeometry_Display.OSPRayScaleFunction = 'PiecewiseFunction'
	simulatorResultsGeometry_Display.SelectOrientationVectors = 'fluidPressureGradient'
	simulatorResultsGeometry_Display.ScaleFactor = 0.05
	simulatorResultsGeometry_Display.SelectScaleArray = 'fluidPressure'
	simulatorResultsGeometry_Display.GlyphType = 'Arrow'
	simulatorResultsGeometry_Display.GlyphTableIndexArray = 'fluidPressure'
	simulatorResultsGeometry_Display.GaussianRadius = 0.0025
	simulatorResultsGeometry_Display.SetScaleArray = ['POINTS', 'fluidPressure']
	simulatorResultsGeometry_Display.ScaleTransferFunction = 'PiecewiseFunction'
	simulatorResultsGeometry_Display.OpacityArray = ['POINTS', 'fluidPressure']
	simulatorResultsGeometry_Display.OpacityTransferFunction = 'PiecewiseFunction'
	simulatorResultsGeometry_Display.DataAxesGrid = 'GridAxesRepresentation'
	simulatorResultsGeometry_Display.SelectionCellLabelFontFile = ''
	simulatorResultsGeometry_Display.SelectionPointLabelFontFile = ''
	simulatorResultsGeometry_Display.PolarAxes = 'PolarAxesRepresentation'
	
	# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
	simulatorResultsGeometry_Display.DataAxesGrid.XTitleFontFile = ''
	simulatorResultsGeometry_Display.DataAxesGrid.YTitleFontFile = ''
	simulatorResultsGeometry_Display.DataAxesGrid.ZTitleFontFile = ''
	simulatorResultsGeometry_Display.DataAxesGrid.XLabelFontFile = ''
	simulatorResultsGeometry_Display.DataAxesGrid.YLabelFontFile = ''
	simulatorResultsGeometry_Display.DataAxesGrid.ZLabelFontFile = ''
	
	# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
	simulatorResultsGeometry_Display.PolarAxes.PolarAxisTitleFontFile = ''
	simulatorResultsGeometry_Display.PolarAxes.PolarAxisLabelFontFile = ''
	simulatorResultsGeometry_Display.PolarAxes.LastRadialAxisTextFontFile = ''
	simulatorResultsGeometry_Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''
	
	# show color bar/color legend
	simulatorResultsGeometry_Display.SetScalarBarVisibility(renderView1, True)
	
	# get opacity transfer function/opacity map for 'fluidPressure'
	fluidPressurePWF = GetOpacityTransferFunction('fluidPressure')
	
	# Properties modified on renderView1
	renderView1.OrientationAxesVisibility = 0
	
	# get the material library
	materialLibrary1 = GetMaterialLibrary()
	
	# Properties modified on renderView1
	renderView1.OrientationAxesVisibility = 1
	
	# turn off scalar coloring
	ColorBy(simulatorResultsGeometry_Display, None)
	
	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(fluidPressureLUT, renderView1)
	
	# change solid color
	simulatorResultsGeometry_Display.DiffuseColor = [0.0, 0.0, 0.0]
	
	# set active source
	SetActiveSource(simulatorResults_)
	
	# Properties modified on renderView1
	renderView1.OrientationAxesVisibility = 0
	
	# current camera placement for renderView1
	renderView1.InteractionMode = '2D'
	renderView1.CameraPosition = [0.0, 0.0, 1.3660254037844388]
	renderView1.CameraParallelScale = .2414817229651483
	
	# save animation
	SaveAnimation(fname_out, renderView1, ImageResolution=[1830, 1166],
	    TransparentBackground=1,
	    FrameWindow=[0, numResults])
	
	#### saving camera placements for all active views
	
	# current camera placement for renderView1
	renderView1.InteractionMode = '2D'
	renderView1.CameraPosition = [0.0, 0.0, 1.3660254037844388]
	renderView1.CameraParallelScale = 0.2414817229651483
	
	#### uncomment the following to render all views
	# RenderAllViews()
	# alternatively, if you want to write images, you can use SaveScreenshot(...).
