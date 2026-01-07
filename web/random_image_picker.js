import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.RandomImagePicker",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "RandomImagePicker") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated?.apply(this, arguments);
                
                // Add file browser button
                const pathWidget = this.widgets.find(w => w.name === "path");
                if (pathWidget) {
                    // Add button to open file dialog
                    const button = this.addWidget("button", "Browse...", null, () => {
                        // Create file input element
                        const input = document.createElement("input");
                        
                        // Get folder_mode widget value
                        const folderModeWidget = this.widgets.find(w => w.name === "folder_mode");
                        const isFolderMode = folderModeWidget?.value || false;
                        
                        if (isFolderMode) {
                            // Folder selection
                            input.type = "file";
                            input.webkitdirectory = true;
                            input.directory = true;
                        } else {
                            // File selection
                            input.type = "file";
                            input.accept = "image/png, image/jpeg, image/webp, image/bmp, image/gif";
                        }
                        
                        input.onchange = (e) => {
                            if (e.target.files && e.target.files[0]) {
                                if (isFolderMode) {
                                    // Get folder path from first file
                                    const firstFile = e.target.files[0];
                                    const fullPath = firstFile.webkitRelativePath || firstFile.name;
                                    const folderPath = fullPath.split('/')[0];
                                    pathWidget.value = folderPath;
                                } else {
                                    // Get file path
                                    const file = e.target.files[0];
                                    // Note: For security reasons, browsers don't expose full file paths
                                    // We can only get the file name, not the full path
                                    // Users will need to manually enter the full path or use relative paths
                                    pathWidget.value = file.name;
                                    
                                    // Show info message
                                    console.log("Note: Due to browser security, full path is not available. Please enter the complete path manually.");
                                }
                            }
                        };
                        
                        input.click();
                    });
                    
                    // Add helper text
                    this.addWidget("text", "helper", "Tip: Enter full path or use ComfyUI input folder", () => {}, {
                        serialize: false
                    });
                }
                
                return result;
            };
        }
    }
});
