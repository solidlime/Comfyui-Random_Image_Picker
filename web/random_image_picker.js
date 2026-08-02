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
                    
                    input.onchange = async (e) => {
                        if (e.target.files && e.target.files[0]) {
                            const file = e.target.files[0];
                            
                            // Automatically switch to Single mode (folder_mode = False)
                            const folderModeWidget = node.widgets.find(w => w.name === "folder_mode");
                            if (folderModeWidget) {
                                folderModeWidget.value = false;
                            }
                            
                            try {
                                // Upload image to ComfyUI temp storage
                                const body = new FormData();
                                body.append('image', file);
                                body.append('type', 'temp');
                                
                                const api = app.api;
                                const fetchFn = api.apiFetch ? api.apiFetch.bind(api) : api.fetchApi.bind(api);
                                const resp = await fetchFn('/upload/image', { method: 'POST', body });
                                if (resp.status !== 200) {
                                    throw new Error(`Upload failed with status ${resp.status}`);
                                }
                                
                                const data = await resp.json();
                                
                                // Store reference string in widget (not base64)
                                const path = data.subfolder ? `${data.subfolder}/${data.name}` : data.name;
                                const ref = `${path} [temp]`;
                                
                                let imageDataWidget = node.widgets.find(w => w.name === "image_data");
                                if (imageDataWidget) {
                                    imageDataWidget.value = ref;
                                }
                                
                                // Show instant preview from temp storage
                                const img = new Image();
                                img.onload = () => {
                                    node.imgs = [img];
                                    node.setSizeForImage?.();
                                    app.graph.setDirtyCanvas(true);
                                };
                                img.src = api.apiURL('/view?filename=' + encodeURIComponent(data.name) + '&type=temp&subfolder=' + encodeURIComponent(data.subfolder || ''));
                            } catch (err) {
                                console.error("[Random Image Picker] Upload failed:", err);
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
