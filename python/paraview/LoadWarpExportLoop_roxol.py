# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`
# -----------------------------------------------------------------------
#
# Script simply loads and displays a 2D .vtu file - the intention of this tracing was to learn the relevant commands for streamlining import, display, filtering, export of roxol result files
#
# -----------------------------------------------------------------------

#### import the simple module from the paraview
from paraview.simple import *
import glob

warping = False
WarpFactor = 100.0

fpath_in = 'E:\\OLE\\roxol\\RESULTS\\90deg_random\\unconfined\\*.vtu'
files = glob.glob(fpath_in)
print(files)

# output files specs
fpath_out = 'E:\\OLE\\roxol\\RESULTS\\plots\\90deg_random\\unconfined\\animations\\simple_network\\'
fname_out = fpath_out + 'FN_result.png'

Transparent_background = 1

res_out = [1830, 1166] #output png resolution
CamPos = [0.0, 0.0, 1.3660254037844388] # Camera position
CamScale = 0.2414817229651483
axis_visibility = 0

# --------- start of loop, don't change below this point unless you exactly know what you are doing!!


#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()
ResetSession()
# create a new 'XML Unstructured Grid Reader'
simulatorResults_ = XMLUnstructuredGridReader(FileName=files)
simulatorResults_.CellArrayStatus = ['element_displacement_$vector_$createComponentsAsScalar', 'element_strain_3esd_$createComponentsAsScalar', 'element_stress_3esd_$createComponentsAsScalar', 'element_principalStress_$vector_$createComponentsAsScalar', 'element_heaviside_$scalar', 'element_radialStress_$scalar', 'element_tangentialStress_$scalar', 'element_shearStress_$scalar', 'element_radialDisplacement_$scalar', 'element_tangentialDisplacement_$scalar', 'element_S1S3Quotient_$scalar', 'element_3S1minusS3_$scalar', 'element_3S3minusS1_$scalar', 'element_principalStress2d_$createComponentsAsScalar', 'element_elasticShearEnergyDensity_$scalar', 'element_porePressure_$scalar', 'element_porePressureGradient_$vector_$createComponentsAsScalar', 'element_fluidVolumeFlow_$vector_$createComponentsAsScalar', 'element_lastPrincipalDirection_$vector', 'element_material_ids_$scalar']
simulatorResults_.PointArrayStatus = ['node_displacement_$vector_$createComponentsAsScalar', 'node_strain_3esd_$createComponentsAsScalar', 'node_stress_3esd_$createComponentsAsScalar', 'node_radialDisplacement_$scalar', 'node_tangentialDisplacement_$scalar', 'node_cylindrical_stress_$createComponentsAsScalar', 'node_principalStrains_$createComponentsAsScalar', 'node_principalStress_$createComponentsAsScalar', 'node_totalDisplacement_$scalar', 'node_maximumShearStress_$scalar', 'node_totalElasticStrainEnergy_$scalar', 'node_volumetricStrainEnergy_$scalar', 'node_deviatoricStrainEnergy_$scalar', 'node_levelsets_phi_$createComponentsAsScalar', 'node_enrichment_$createComponentsAsScalar', 'node_porePressure_$scalar', 'node_porePressureGradient_$vector_$createComponentsAsScalar', 'node_fluidVolumeFlow_$vector_$createComponentsAsScalar', 'node_averageSubResultDeviation_$scalar', 'node_maximalSubResultDeviation_$scalar']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1830, 1166]

# show data in view
simulatorResults_Display = Show(simulatorResults_, renderView1)

# trace defaults for the display properties.
simulatorResults_Display.Representation = 'Surface'
simulatorResults_Display.ColorArrayName = [None, ''] #None probably sets Solid Color
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

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = CamPos

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = CamPos
renderView1.CameraParallelScale = CamScale

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

# -------------------------- WARP FILTER --------------------------------

if warping == True:
    # find source
    simulatorResults_ = FindSource('simulatorResults_*')

    # create a new 'Warp By Vector'
    warpByVector1 = WarpByVector(Input=simulatorResults_)
    warpByVector1.Vectors = ['POINTS', 'node_displacement_$vector_$createComponentsAsScalar']

    # Properties modified on warpByVector1 --> DEFAULT is 1, but here set to 100 for later image processing
    warpByVector1.ScaleFactor = WarpFactor

    # get active source.
    warpByVector1 = GetActiveSource()

    # set active source
    SetActiveSource(warpByVector1)

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
    # uncomment following to set a specific view size
    # renderView1.ViewSize = [2267, 578]

    # show data in view
    warpByVector1Display = Show(warpByVector1, renderView1)
    # trace defaults for the display properties.
    warpByVector1Display.Representation = 'Surface'
    warpByVector1Display.ColorArrayName = ['CELLS', 'element_material_ids_$scalar']
    warpByVector1Display.OSPRayScaleArray = 'node_averageSubResultDeviation_$scalar'
    warpByVector1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    warpByVector1Display.SelectOrientationVectors = 'None'
    warpByVector1Display.ScaleFactor = 0.0500002394472
    warpByVector1Display.SelectScaleArray = 'None'
    warpByVector1Display.GlyphType = 'Arrow'
    warpByVector1Display.GlyphTableIndexArray = 'None'
    warpByVector1Display.GaussianRadius = 0.00250001197236
    warpByVector1Display.SetScaleArray = ['POINTS', 'node_averageSubResultDeviation_$scalar']
    warpByVector1Display.ScaleTransferFunction = 'PiecewiseFunction'
    warpByVector1Display.OpacityArray = ['POINTS', 'node_averageSubResultDeviation_$scalar']
    warpByVector1Display.OpacityTransferFunction = 'PiecewiseFunction'
    warpByVector1Display.DataAxesGrid = 'GridAxesRepresentation'
    warpByVector1Display.SelectionCellLabelFontFile = ''
    warpByVector1Display.SelectionPointLabelFontFile = ''
    warpByVector1Display.PolarAxes = 'PolarAxesRepresentation'
    warpByVector1Display.ScalarOpacityUnitDistance = 0.01380015219178499

    # init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
    warpByVector1Display.DataAxesGrid.XTitleFontFile = ''
    warpByVector1Display.DataAxesGrid.YTitleFontFile = ''
    warpByVector1Display.DataAxesGrid.ZTitleFontFile = ''
    warpByVector1Display.DataAxesGrid.XLabelFontFile = ''
    warpByVector1Display.DataAxesGrid.YLabelFontFile = ''
    warpByVector1Display.DataAxesGrid.ZLabelFontFile = ''

    # init the 'PolarAxesRepresentation' selected for 'PolarAxes'
    warpByVector1Display.PolarAxes.PolarAxisTitleFontFile = ''
    warpByVector1Display.PolarAxes.PolarAxisLabelFontFile = ''
    warpByVector1Display.PolarAxes.LastRadialAxisTextFontFile = ''
    warpByVector1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

    # hide data in view
    # Hide(simulatorResults_, renderView1)

    # update the view to ensure updated data information
    renderView1.Update()

    #### saving camera placements for all active views

    # current camera placement for renderView1
    renderView1.InteractionMode = '2D'
    renderView1.CameraPosition = [0.0, 0.0, 10000.0]
    renderView1.CameraParallelScale = 0.3535533905932738

    #### uncomment the following to render all views
    # RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).

# --------------------------------- SAVE TO PNGs ------------------------------

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [2267, 823]

# current camera placement for renderView1
# Properties modified on renderView1
renderView1.OrientationAxesVisibility = axis_visibility

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = CamPos
renderView1.CameraParallelScale = 0.2414817229651483

# save animation
SaveAnimation(fname_out, renderView1, ImageResolution=res_out,
    TransparentBackground=Transparent_background,
    FrameWindow=[0, 56])

#### saving camera placements for all active views

# current camera placement for renderView1
# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [0.0, 0.0, 1.3660254037844388]
renderView1.CameraParallelScale = CamScale

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
