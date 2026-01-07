import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Comfy.RandomImagePicker",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "RandomImagePicker") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                const node = this;
                
                // Add browse button
                node.addWidget("button", "📁 Choose File", null, () => {
                    const input = document.createElement("input");
                    input.type = "file";
                    input.accept = "image/png,image/jpeg,image/jpg,image/webp,image/bmp,image/gif";
                    
                    input.onchange = (e) => {
                        if (e.target.files && e.target.files[0]) {
                            const file = e.target.files[0];
                            const imageWidget = node.widgets.find(w => w.name === "image");
                            
                            if (imageWidget) {
                                // Update with file name (user needs to provide full path)
                                imageWidget.value = file.name;
                                console.log("Selected file:", file.name);
                                alert(`File selected: ${file.name}\n\nPlease enter the full path to this file in the text field above.`);
                            }
                        }
                    };
                    
                    input.click();
                });
                
                return result;
            };
        }
    }
});
