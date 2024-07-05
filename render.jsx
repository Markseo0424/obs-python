var jsonPath = "./render.json"

// Custom function to convert a JavaScript object to a JSON string
function serializeToJSON(obj) {
    if (typeof obj !== "object" || obj === null) {
        // If obj is a string, number, boolean, or null, return the appropriate JSON value
        if (typeof obj === "string") {
            return '"' + obj.replace(/"/g, '\\"') + '"';
        }
        return String(obj);
    } else {
        // If obj is an array
        if (Array.isArray(obj)) {
            var json = [];
            for (var i = 0; i < obj.length; i++) {
                json.push(serializeToJSON(obj[i]));
            }
            return "[" + json.join(",") + "]";
        } else {
            // If obj is an object
            var json = [];
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    json.push('"' + key + '":' + serializeToJSON(obj[key]));
                }
            }
            return "{" + json.join(",") + "}";
        }
    }
}

// Function to write a JSON string to a file
function writeJSONToFile(jsonString, filePath) {
    var file = new File(filePath);
    if (file.open("w")) {
        file.write(jsonString);
        file.close();
//         alert("File written successfully: " + filePath);
    } else {
//         alert("Failed to open the file: " + filePath);
    }
}

// Function to read and parse a JSON file
function readJSONFile(filePath) {
    var file = new File(filePath);
    file.encoding = "UTF8";
    var content = "";

    if (file.open("r")) {
        content = file.read();
        file.close();
    } else {
//         alert("Failed to open the file.");
        return null;
    }

    try {
        return JSON.parse(content);
    } catch (e) {
//         alert("Failed to parse JSON: " + e.message);
        return null;
    }
}

// Function to find a composition by name
function findCompByName(compName) {
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem && item.name === compName) {
            return item;
        }
    }
    return null;
}

var renderStatus = {
    "status" : false
}

writeJSONToFile(serializeToJSON(renderStatus),"./renderStatus.json")

// alert("start")

var jsonData = readJSONFile(jsonPath)

// alert("read json")

var myComp = findCompByName(jsonData.compName)

// alert("find comp")

// RENDER
var renderQueueItem = app.project.renderQueue.items.add(myComp);

var lastRenderQueueItemIndex = app.project.renderQueue.numItems;
var outputModule = app.project.renderQueue.item(lastRenderQueueItemIndex).outputModule(1);


var outputFile = new File(jsonData.filePath);

if (outputFile.exists && jsonData.replaceExist) {
    outputFile.remove()
}

// Set the output file path
outputModule.file = outputFile

// Apply output module template
// outputModule.applyTemplate("High Quality"); // Adjust this to the nearest template you have
outputModule.applyTemplate(jsonData.renderTemplate);

renderQueueItem.onStatusChanged = function() {
            if (renderQueueItem.status === RQItemStatus.DONE) {
                var renderStatus = {
                    "status" : true
                }

                writeJSONToFile(serializeToJSON(renderStatus),"./renderStatus.json")
//                 alert("Rendering completed successfully: " + outputPath);
            } else if (renderQueueItem.status === RQItemStatus.ERR_STOPPED) {
//                 alert("Rendering failed.");
            }
        };

// Render the composition
app.project.renderQueue.render(); // render in after effects