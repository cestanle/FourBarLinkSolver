import adsk.core, adsk.fusion, traceback
import csv
import os

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct
        
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox('No active design')
            return
        
        rootComp = design.rootComponent
        
        # Get first sketch
        if rootComp.sketches.count == 0:
            ui.messageBox('No sketches found.')
            return
        
        sketch = rootComp.sketches.item(0)
        
        # Find first spline
        spline = None
        for curve in sketch.sketchCurves:
            if curve.objectType == adsk.fusion.SketchFittedSpline.classType():
                spline = curve
                break
        
        if spline is None:
            ui.messageBox('No fitted spline found in sketch.')
            return
        
        # Number of sample points
        num_samples = 100
        
        # Get parameter range
        evaluator = spline.geometry.evaluator
        success, startParam, endParam = evaluator.getParameterExtents()
        
        if not success:
            ui.messageBox('Could not get spline parameter range.')
            return
        
        # Sample points
        points = []
        for i in range(num_samples):
            t = startParam + (endParam - startParam) * i / (num_samples - 1)
            success, point = evaluator.getPointAtParameter(t)
            if success:
                points.append([point.x, point.y])
        
        # Save CSV to desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, "spline_points.csv")
        
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['x', 'y'])
            writer.writerows(points)
        
        ui.messageBox(f'Success!\nSaved to:\n{file_path}')
    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
