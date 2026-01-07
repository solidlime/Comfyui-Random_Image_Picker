import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

app.registerExtension({
    name: "Comfy.RandomImagePicker",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "RandomImagePicker") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const ret = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Find the image widget
                const imageWidget = this.widgets.find(w => w.name === "image");
                if (!imageWidget) return ret;
                
                // Create file input button widget
                const fileWidget = this.addWidget("button", "📁 Choose File", "file", () => {
                    const input = document.createElement("input");
                    input.type = "file";
                    input.accept = "image/png,image/jpeg,image/jpg,image/webp,image/bmp,image/gif";
                    
                    input.onchange = (e) => {
                        if (e.target.files && e.target.files[0]) {
                            const file = e.target.files[0];
                            
                            // Create a URL for the file
                            const reader = new FileReader();
                            reader.onload = (event) => {
                                // Get file path (name only, browser security limitation)
                                const fileName = file.name;
                                
                                // Try to use the webkitRelativePath or fall back to name
                                const filePath = file.webkitRelativePath || file.path || fileName;
                                
                                // Update the image widget value
                                imageWidget.value = filePath;
                                
                                console.log("Selected file:", filePath);
                                
                                // Show notification
                                app.ui.dialog.show(`File selected: ${fileName}\n\nNote: You may need to enter the full path manually due to browser security restrictions.`);
                            };
                            reader.readAsDataURL(file);
                        }
                    };
                    
                    input.click();
                });
                
                // Add info widget
                const infoWidget = this.addWidget("text", "ℹ️ Info", 
                    "Single mode: Select any image file\nFolder mode: File's folder will be used", 
                    () => {}, 
                    { serialize: false }
                );
                
                return ret;
            };
        }
    }
});
