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
                                // Show selected file name
                                const fileName = file.name;
                                console.log("Selected file:", fileName);
                                
                                // Show dialog with instructions
                                const currentPath = imageWidget.value || "";
                                const dialogText = `File selected: ${fileName}\n\n` +
                                    `⚠️ IMPORTANT:\n` +
                                    `Due to browser security, the full path cannot be automatically detected.\n\n` +
                                    `Please copy and paste the FULL PATH to this file in the 'image' field above.\n\n` +
                                    `Example:\n` +
                                    `D:\\Images\\${fileName}\n` +
                                    `or\n` +
                                    `C:\\Users\\YourName\\Pictures\\${fileName}\n\n` +
                                    `Current default: ${currentPath || '(not set)'}`;
                                
                                alert(dialogText);
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
