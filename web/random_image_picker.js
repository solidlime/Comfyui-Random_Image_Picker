import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.RandomImagePicker",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "RandomImagePicker") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                const node = this;
                
                // Add file picker button
                node.addWidget("button", "📁 Choose File", null, () => {
                    const input = document.createElement("input");
                    input.type = "file";
                    input.accept = "image/png,image/jpeg,image/jpg,image/webp,image/bmp,image/gif";
                    
                    input.onchange = (e) => {
                        if (e.target.files && e.target.files[0]) {
                            const file = e.target.files[0];
                            
                            // Automatically switch to Single mode (folder_mode = False)
                            const folderModeWidget = node.widgets.find(w => w.name === "folder_mode");
                            if (folderModeWidget) {
                                folderModeWidget.value = false;
                                console.log("[Random Image Picker] Switched to Single mode");
                            }
                            
                            // Read file as base64
                            const reader = new FileReader();
                            reader.onload = (event) => {
                                const base64Data = event.target.result;
                                
                                // Find or create the image_data widget
                                let imageDataWidget = node.widgets.find(w => w.name === "image_data");
                                if (imageDataWidget) {
                                    imageDataWidget.value = base64Data;
                                }
                                
                                console.log(`[Random Image Picker] File loaded: ${file.name} (${(base64Data.length / 1024).toFixed(2)} KB)`);
                                alert(`✅ Image loaded successfully!\n\nFile: ${file.name}\nSize: ${(file.size / 1024).toFixed(2)} KB\n\nMode: Automatically switched to Single\n\nYou can now run the workflow.`);
                            };
                            
                            reader.onerror = () => {
                                alert("❌ Failed to read the image file.\n\nPlease try again.");
                            };
                            
                            reader.readAsDataURL(file);
                        }
                    };
                    
                    input.click();
                });
                
                return result;
            };
        }
    }
});
