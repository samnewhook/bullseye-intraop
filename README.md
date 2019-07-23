# Bullseye - Computer Vision for the glenoid implant in total shoulder arthroplasty

## Key Investigators
- David M. Burns, MD, PhD(c) (Sunnybrook Research Institute) 
- Samuel C.P. Newhook, BASc (Sunnybrook Research Institute) 
- Cari Whyne, PhD (Sunnybrook Research Institute)

# Project Description
Positioning of the glenoid component in total shoulder arthroplasty is a challenging and important step for the longevity and functional outcomes of the surgery. This project aims to provide intraoperative validation for implant positioning.

## Objective
1. Enable automatic validation of glenoid implant placement using 3D scanning technology (Einscan Pro). Surgeons must be able to take a scan and receive a validation results within 3 minutes of guidewire placement.
2. Automatic import of optical scan into slicer. As it stands, the optical image must be taken and loaded manually.

## Approach and Plan
1. Targeting the automation of intra-operative image processing steps. These are as follows:
    1. Segmentation of tracker and glenoid from intra-operative optical image 
    2. Pre-alignment for optical tracker registration
    3. Optical tracker registration (surface based) 
    4. Validation of tracker registration (visual / numeric)
    5. Pre-alignment for glenoid optical image to pre-operative mesh model
    6. Glenoid registration (surface based) 
    7. Validation of glenoid registration (visual / numeric)
    8. Visualize prediction 
2. Define data flow for each step (inputs and outputs)
3. Create modules for each step or grouping of 2-3 steps
4. Create a workflow module for linking steps (handle workflow logic)

## Progress and Next Steps
<!--Describe progress and next steps in a few bullet points as you are making progress.-->
Created simple data flow diagram for the first module. Next is to sketchup module design and implement in Slicer.

### Notes
The shape of the marker is essentially a cone with the top cut off. The optical image only needs to capture the curved face to some degree. The gradient of the curvature ensures that an incomplete surface area captured will be enough to constrain the surface registration along the length of the cone. Due to the symmetrical nature of the wire and tracker, the surface registration of the optical image face to the model face does not need to be constrained around the radius of the tracker face. 

# Illustrations

<!--Add pictures and links to videos that demonstrate what has been accomplished.-->

<!--![Description of picture](Example2.jpg)-->
[Data Flow Diagram for Module 1: Prealign optical image of tracker and tracker model](image_resources/Bullseye_Data_Flow_Module_1.png)
<!--![Some more images](Example2.jpg)-->

# Background and References

<!--Use this space for information that may help people better understand your project, like links to papers, source code, or data.-->
