cmake_minimum_required(VERSION 3.5)

project(BullseyeIntraOp)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/BullseyeIntraOp")
set(EXTENSION_CATEGORY "Bullseye")
set(EXTENSION_CONTRIBUTORS "Samuel C.P. Newhook (Sunnybrook Research Institute)")
set(EXTENSION_DESCRIPTION "Intraop workflow for automatic evaluation of wire placement for total shoulder arthroplasty.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/BullseyeIntraOp.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/BullseyeIntraOp/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(PreAlignTracker)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
