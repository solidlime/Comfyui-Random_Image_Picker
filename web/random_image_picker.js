import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.RandomImagePicker",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "RandomImagePicker") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                const node = this;
                
                // Completely hide image_data widget
                setTimeout(() => {
                    const imageDataWidget = node.widgets.find(w => w.name === "image_data");
                    if (imageDataWidget) {
                        imageDataWidget.type = "converted-widget";
                        imageDataWidget.hidden = true;
                        imageDataWidget.computeSize = () => [0, -4];
                        imageDataWidget.serializeValue = () => imageDataWidget.value;
                    }
                }, 10);
                
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
                            }
                            
                            // Read file as base64
                            const reader = new FileReader();
                            reader.onload = (event) => {
                                const base64Data = event.target.result;
                                
                                // Store image_data in widget
                                let imageDataWidget = node.widgets.find(w => w.name === "image_data");
                                if (imageDataWidget) {
                                    imageDataWidget.value = base64Data;
                                }
                                
                                // Show instant preview
                                const img = new Image();
                                img.onload = () => {
                                    node.imgs = [img];
                                    node.setSizeForImage?.();
                                    app.graph.setDirtyCanvas(true);
                                };
                                img.src = base64Data;
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
