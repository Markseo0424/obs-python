// Create a new composition
var compWidth = 1920;
var compHeight = 1080;
var compPixelAspect = 1.0;
var compDuration = 10; // Duration in seconds
var compFrameRate = 30; // Frame rate


var myComp = app.project.items.addComp("Centered Text Composition Second", compWidth, compHeight, compPixelAspect, compDuration, compFrameRate);

// Add a text layer
var textLayer = myComp.layers.addText("Centered Text");

// Get the text layer's property for the text source
var textProp = textLayer.property("Source Text");
var textDocument = textProp.value;
textDocument.justification = ParagraphJustification.CENTER_JUSTIFY;
textProp.setValue(textDocument);

// Center the text layer in the composition
textLayer.position.setValue([compWidth / 2, compHeight / 2]);

// Optionally, you can set additional properties for the text
textDocument.fontSize = 100;
textProp.setValue(textDocument);


// RENDER
var renderQueueItem = app.project.renderQueue.items.add(myComp);

var lastRenderQueueItemIndex = app.project.renderQueue.numItems;
var outputModule = app.project.renderQueue.item(lastRenderQueueItemIndex).outputModule(1);


// Set the output file path
outputModule.file = new File("~/Desktop/render_output.mov");

// Apply output module template
// Use "H.264" if it's available or set up as a custom template, otherwise, this is a general setup
outputModule.applyTemplate("High Quality"); // Adjust this to the nearest template you have

// If you have a custom output module template for H.264, use it here
// outputModule.applyTemplate("H.264"); // Custom template name

// Render the composition
// app.project.renderQueue.queueInAME(true); // set to true to instant render
app.project.renderQueue.render(); // render in after effects