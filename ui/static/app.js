const elements = {
    systemDot: document.querySelector("#systemDot"),
    systemStatus: document.querySelector("#systemStatus"),
    productSelect: document.querySelector("#productSelect"),
    selectedProductId: document.querySelector("#selectedProductId"),
    generateButton: document.querySelector("#generateButton"),
    runMessage: document.querySelector("#runMessage"),
    runStatus: document.querySelector("#runStatus"),
    generationStatus: document.querySelector("#generationStatus"),
    auditScore: document.querySelector("#auditScore"),
    promptLength: document.querySelector("#promptLength"),
    previewBadge: document.querySelector("#previewBadge"),
    emptyPreview: document.querySelector("#emptyPreview"),
    generatedImage: document.querySelector("#generatedImage"),
    detailProduct: document.querySelector("#detailProduct"),
    detailSize: document.querySelector("#detailSize"),
    detailPrice: document.querySelector("#detailPrice"),
    detailScene: document.querySelector("#detailScene"),
    detailMaterial: document.querySelector("#detailMaterial"),
    detailEngine: document.querySelector("#detailEngine"),
    artifactList: document.querySelector("#artifactList"),
    promptPreview: document.querySelector("#promptPreview"),
    copyPromptButton: document.querySelector("#copyPromptButton"),
    openProductDialog: document.querySelector("#openProductDialog"),
    editProductButton: document.querySelector("#editProductButton"),
    productDialogMode: document.querySelector("#productDialogMode"),
    productDialogTitle: document.querySelector("#productDialogTitle"),
    productIdInput: document.querySelector('#productForm input[name="product_id"]'),
    productDialog: document.querySelector("#productDialog"),
    productForm: document.querySelector("#productForm"),
    closeProductDialog: document.querySelector("#closeProductDialog"),
    cancelProductDialog: document.querySelector("#cancelProductDialog"),
    createProductButton: document.querySelector("#createProductButton"),
    productFormMessage: document.querySelector("#productFormMessage"),
    productImageInput: document.querySelector('#productForm input[name="image"]'),
    productImagePreview: document.querySelector("#productImagePreview"),
    productImagePreviewImage: document.querySelector("#productImagePreviewImage"),
    productImagePreviewName: document.querySelector("#productImagePreviewName"),
};

let currentPrompt = "";
let productImagePreviewUrl = null;
let editingProductId = null;

async function fetchJson(url, options = {}) {
    const response = await fetch(url, options);
    const body = await response.json();

    return {
        response,
        body,
    };
}

async function loadProductDetails(productId) {
    if (!productId) {
        elements.detailProduct.textContent = "—";
        elements.detailSize.textContent = "—";
        elements.detailPrice.textContent = "—";
        elements.detailMaterial.textContent = "—";
        elements.editProductButton.disabled = true;
        return;
    }

    elements.editProductButton.disabled = false;

    try {
        const { response, body } = await fetchJson(
            `/products/${encodeURIComponent(productId)}`
        );

        if (!response.ok) {
            throw new Error(
                body.detail || "تعذر تحميل بيانات المنتج."
            );
        }

        const size = (
            body.size && typeof body.size === "object"
                ? body.size
                : {}
        );

        const dimensions = [
            size.width,
            size.height,
            size.depth,
        ].filter(
            (value) => (
                value !== undefined
                && value !== null
                && value !== ""
            )
        );

        const material = (
            body.material
            && typeof body.material === "object"
                ? body.material.primary
                : body.material
        );

        const pricing = (
            body.pricing
            && typeof body.pricing === "object"
                ? body.pricing
                : {}
        );

        elements.detailProduct.textContent = (
            body.name || body.id
        );

        elements.detailSize.textContent = (
            dimensions.length
                ? dimensions.join(" × ")
                : "—"
        );

        elements.detailMaterial.textContent = (
            material || "—"
        );

        elements.detailPrice.textContent = (
            pricing.price !== undefined
                ? `${pricing.price} ${pricing.currency || ""}`.trim()
                : "—"
        );
    } catch (error) {
        elements.detailProduct.textContent = productId;
        elements.detailSize.textContent = "—";
        elements.detailPrice.textContent = "—";
        elements.detailMaterial.textContent = "—";
    }
}

function setMessage(message, type = "") {
    elements.runMessage.textContent = message;
    elements.runMessage.className = "run-message";

    if (type) {
        elements.runMessage.classList.add(type);
    }
}

function setBadge(label, type = "neutral") {
    elements.previewBadge.textContent = label;
    elements.previewBadge.className = `badge ${type}`;
}

function setLoading(isLoading) {
    elements.generateButton.disabled = (
        isLoading
        || !elements.productSelect.value
    );

    elements.productSelect.disabled = isLoading;

    if (isLoading) {
        elements.generateButton.querySelector(
            "span"
        ).textContent = "جاري تشغيل النظام...";
    } else {
        elements.generateButton.querySelector(
            "span"
        ).textContent = "بدء تشغيل النظام";
    }
}

function clearImage() {
    elements.generatedImage.hidden = true;
    elements.generatedImage.removeAttribute("src");
    elements.emptyPreview.hidden = false;
}

function showReferenceImage(productId) {
    if (!productId) {
        clearImage();
        return;
    }

    elements.generatedImage.onerror = () => {
        clearImage();
        setBadge("لا توجد صورة مرجعية", "error");
    };

    elements.generatedImage.src = (
        `/products/${encodeURIComponent(productId)}/image`
        + `?t=${Date.now()}`
    );

    elements.generatedImage.alt = (
        `الصورة الأصلية للمنتج ${productId}`
    );

    elements.generatedImage.hidden = false;
    elements.emptyPreview.hidden = true;

    setBadge("الصورة الأصلية", "neutral");
}

function outputUrl(productId, artifactPath) {
    if (!artifactPath) {
        return null;
    }

    const normalized = String(artifactPath).replaceAll(
        "\\",
        "/"
    );

    const prefix = `outputs/${productId}/`;

    if (!normalized.startsWith(prefix)) {
        return null;
    }

    const relativePath = normalized.slice(prefix.length);

    const encodedPath = relativePath
        .split("/")
        .map(encodeURIComponent)
        .join("/");

    return (
        `/outputs/${encodeURIComponent(productId)}`
        + `/${encodedPath}`
    );
}

function renderArtifacts(productId, artifacts = {}) {
    elements.artifactList.innerHTML = "";

    const entries = Object.entries(artifacts);

    if (!entries.length) {
        elements.artifactList.innerHTML = (
            '<p class="muted">لا توجد ملفات مسجلة.</p>'
        );
        return;
    }

    for (const [name, path] of entries) {
        if (Array.isArray(path)) {
            path.forEach((item, index) => {
                addArtifactLink(
                    productId,
                    `${name} ${index + 1}`,
                    item
                );
            });
        } else {
            addArtifactLink(productId, name, path);
        }
    }
}

function addArtifactLink(productId, name, path) {
    const url = outputUrl(productId, path);

    if (!url) {
        return;
    }

    const link = document.createElement("a");
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";

    const label = document.createElement("span");
    label.textContent = name.replaceAll("_", " ");

    const arrow = document.createElement("span");
    arrow.textContent = "↗";

    link.append(label, arrow);
    elements.artifactList.append(link);
}

function clearRunResult() {
    elements.runStatus.textContent = "جاهز";
    elements.generationStatus.textContent = "—";
    elements.auditScore.textContent = "—";
    elements.promptLength.textContent = "—";

    elements.detailScene.textContent = "—";
    elements.detailEngine.textContent = "—";

    currentPrompt = "";

    elements.promptPreview.textContent = (
        "لم يتم إنشاء برومبت بعد."
    );

    elements.copyPromptButton.disabled = true;

    elements.artifactList.innerHTML = (
        '<p class="muted">'
        + "لا توجد ملفات بعد."
        + "</p>"
    );
}

function renderManifest(manifest) {
    const productId = manifest.product_id;
    const run = manifest.run || {};
    const generation = manifest.generation || {};
    const designDna = manifest.design_dna || {};
    const prompt = manifest.prompt || {};
    const audit = prompt.audit || {};
    const score = audit.score || {};

    elements.runStatus.textContent = (
        run.status || "unknown"
    );

    elements.generationStatus.textContent = (
        generation.status || "unknown"
    );

    elements.auditScore.textContent = (
        score.percentage !== undefined
            ? `${score.percentage}%`
            : "—"
    );

    currentPrompt = prompt.text || "";

    elements.promptLength.textContent = (
        currentPrompt
            ? `${currentPrompt.length} حرف`
            : "—"
    );

    elements.promptPreview.textContent = (
        currentPrompt
        || "لم يتم إنشاء برومبت بعد."
    );

    elements.copyPromptButton.disabled = !currentPrompt;

    elements.detailScene.textContent = (
        designDna.scene || "—"
    );

    elements.detailEngine.textContent = (
        run.engine_name
        || generation.engine
        || "—"
    );

    renderArtifacts(
        productId,
        manifest.artifacts || {}
    );

    const imagePath = generation.image;
    const imageUrl = outputUrl(productId, imagePath);

    if (imageUrl && generation.status === "success") {
        elements.generatedImage.src = (
            `${imageUrl}?t=${Date.now()}`
        );
        elements.generatedImage.hidden = false;
        elements.emptyPreview.hidden = true;
        setBadge("تم إنتاج الصورة", "success");
    } else {
        showReferenceImage(productId);

        setBadge(
            "الصورة الأصلية — لم يتم التوليد",
            "error"
        );
    }

    if (run.status === "succeeded") {
        setMessage(
            "اكتمل تشغيل المنتج بنجاح.",
            "success"
        );
    } else if (generation.status === "local_only") {
        setMessage(
            "اكتمل التحليل والبرومبت، لكن محرك الصور "
            + "غير متاح لعدم وجود مفتاح حقيقي.",
            "error"
        );
    } else {
        const errorMessage = (
            run.error?.message
            || "لم يكتمل تشغيل المنتج."
        );

        setMessage(errorMessage, "error");
    }
}

async function loadManifest(
    productId,
    allowMissing = false
) {
    const url = (
        `/runs/${encodeURIComponent(productId)}/latest`
    );

    const { response, body } = await fetchJson(url);

    if (
        response.status === 404
        && allowMissing
    ) {
        clearRunResult();
        return false;
    }

    if (!response.ok) {
        throw new Error(
            body.detail || "تعذر تحميل manifest."
        );
    }

    renderManifest(body);
    return true;
}

async function loadLatestManifest(productId) {
    if (!productId) {
        return;
    }

    try {
        await loadManifest(
            productId,
            true
        );
    } catch (error) {
        // No saved run exists for this product yet.
    }
}

async function loadSystemStatus() {
    try {
        const { response, body } = await fetchJson(
            "/system/readiness"
        );

        if (!response.ok) {
            throw new Error(
                "System unavailable"
            );
        }

        const imageEngine = (
            body.image_engine || {}
        );

        elements.systemDot.classList.add(
            "online"
        );

        elements.systemStatus.textContent = (
            imageEngine.configured
                ? "AI Furniture OS — محرك الصور جاهز"
                : "AI Furniture OS — متصل / وضع محلي"
        );

        elements.systemStatus.title = (
            `${imageEngine.name || "image engine"}`
            + ` — ${imageEngine.model || "no model"}`
        );
    } catch (error) {
        elements.systemDot.classList.add(
            "offline"
        );

        elements.systemStatus.textContent = (
            "النظام غير متصل"
        );
    }
}

async function loadProducts(
    preferredProductId = "Partition001"
) {
    try {
        const { response, body } = await fetchJson(
            "/products"
        );

        if (!response.ok) {
            throw new Error(
                body.detail || "تعذر تحميل المنتجات."
            );
        }

        elements.productSelect.innerHTML = (
            '<option value="">اختر المنتج</option>'
        );

        for (const product of body.products) {
            const option = document.createElement(
                "option"
            );

            option.value = product.id;
            option.textContent = (
                product.name
                    ? `${product.name} — ${product.id}`
                    : product.id
            );

            elements.productSelect.append(option);
        }

        if (!body.products.length) {
            elements.productSelect.innerHTML = (
                '<option value="">لا توجد منتجات</option>'
            );
            elements.editProductButton.disabled = true;
        } else {
            const preferredProduct = (
                body.products.find(
                    (product) => (
                        product.id === preferredProductId
                    )
                )
                || body.products.find(
                    (product) => (
                        product.id === "Partition001"
                    )
                )
                || body.products[0]
            );

            elements.productSelect.value = preferredProduct.id;
            elements.selectedProductId.textContent = preferredProduct.id;
            elements.generateButton.disabled = false;
            elements.editProductButton.disabled = false;

            setMessage("المنتج جاهز لبدء الإنتاج.");
            showReferenceImage(preferredProduct.id);
            await loadProductDetails(preferredProduct.id);
            await loadLatestManifest(
                preferredProduct.id
            );
        }
    } catch (error) {
        elements.productSelect.innerHTML = (
            '<option value="">تعذر تحميل المنتجات</option>'
        );
        elements.editProductButton.disabled = true;

        setMessage(error.message, "error");
    }
}

function clearProductImagePreview() {
    if (productImagePreviewUrl) {
        URL.revokeObjectURL(productImagePreviewUrl);
        productImagePreviewUrl = null;
    }

    elements.productImagePreview.hidden = true;
    elements.productImagePreviewImage.removeAttribute("src");
    elements.productImagePreviewName.textContent = "";
}

function closeProductFormDialog() {
    clearProductImagePreview();
    editingProductId = null;
    elements.productDialog.close();
    elements.productFormMessage.textContent = "";
    elements.productFormMessage.className = (
        "form-message"
    );
}

elements.productImageInput.addEventListener(
    "change",
    () => {
        clearProductImagePreview();

        const file = elements.productImageInput.files[0];

        if (!file) {
            return;
        }

        if (!file.type.startsWith("image/")) {
            elements.productFormMessage.textContent = (
                "الملف المختار ليس صورة صالحة."
            );

            elements.productFormMessage.className = (
                "form-message error"
            );

            elements.productImageInput.value = "";
            return;
        }

        productImagePreviewUrl = URL.createObjectURL(file);
        elements.productImagePreviewImage.src = productImagePreviewUrl;
        elements.productImagePreviewName.textContent = file.name;
        elements.productImagePreview.hidden = false;
    }
);

elements.openProductDialog.addEventListener(
    "click",
    () => {
        editingProductId = null;
        elements.productForm.reset();
        clearProductImagePreview();
        elements.productIdInput.disabled = false;
        elements.productImageInput.required = true;
        elements.productDialogMode.textContent = "NEW PRODUCT";
        elements.productDialogTitle.textContent = "إضافة منتج جديد";
        elements.createProductButton.textContent = "إنشاء المنتج";
        elements.productFormMessage.textContent = "";
        elements.productFormMessage.className = (
            "form-message"
        );
        elements.productDialog.showModal();
    }
);

elements.editProductButton.addEventListener(
    "click",
    async () => {
        const productId = elements.productSelect.value;
        if (!productId) {
            return;
        }

        editingProductId = productId;
        elements.productForm.reset();
        clearProductImagePreview();
        elements.productFormMessage.textContent = "";
        elements.productFormMessage.className = "form-message";

        elements.productDialogMode.textContent = "EDIT PRODUCT";
        elements.productDialogTitle.textContent = "تعديل المنتج";
        elements.createProductButton.textContent = "حفظ التعديلات";
        elements.productIdInput.value = productId;
        elements.productIdInput.disabled = true;

        elements.productImageInput.required = false;

        try {
            const { response, body } = await fetchJson(
                `/products/${encodeURIComponent(productId)}`
            );

            if (response.ok) {
                elements.productForm.querySelector('input[name="name"]').value = body.name || "";
                elements.productForm.querySelector('input[name="category"]').value = body.category || "";

                const material = body.material && typeof body.material === "object" ? body.material.primary : body.material;
                elements.productForm.querySelector('input[name="material"]').value = material || "";

                const size = body.size || {};
                elements.productForm.querySelector('input[name="width"]').value = size.width || "";
                elements.productForm.querySelector('input[name="height"]').value = size.height || "";
                elements.productForm.querySelector('input[name="depth"]').value = size.depth || "";

                const pricing = body.pricing || {};
                elements.productForm.querySelector('input[name="price"]').value = pricing.price || "";

                const currencySelect = elements.productForm.querySelector('select[name="currency"]');
                if (currencySelect) {
                    currencySelect.value = pricing.currency || "KWD";
                }
            }
        } catch (error) {
            // Ignore pre-fill errors if any
        }

        elements.productDialog.showModal();
    }
);

elements.closeProductDialog.addEventListener(
    "click",
    closeProductFormDialog
);

elements.cancelProductDialog.addEventListener(
    "click",
    closeProductFormDialog
);

elements.productForm.addEventListener(
    "submit",
    async (event) => {
        event.preventDefault();

        const isEditing = Boolean(editingProductId);
        const originalLabel = elements.createProductButton.textContent;

        elements.createProductButton.disabled = true;
        elements.createProductButton.textContent = isEditing
            ? "جاري حفظ التعديلات..."
            : "جاري إنشاء المنتج...";

        elements.productFormMessage.textContent = "";
        elements.productFormMessage.className = "form-message";

        try {
            const formData = new FormData(elements.productForm);

            let url = "/products";
            let method = "POST";

            if (isEditing) {
                url = `/products/${encodeURIComponent(editingProductId)}`;
                method = "PUT";
                formData.delete("product_id");

                const imageFile = elements.productImageInput.files[0];
                if (!imageFile) {
                    formData.delete("image");
                }
            }

            const { response, body } = await fetchJson(
                url,
                {
                    method: method,
                    body: formData,
                }
            );

            if (!response.ok) {
                const message = (
                    typeof body.detail === "string"
                        ? body.detail
                        : (isEditing ? "تعذر تعديل المنتج." : "تعذر إنشاء المنتج.")
                );

                throw new Error(message);
            }

            elements.productFormMessage.textContent = isEditing
                ? "تم تعديل المنتج بنجاح."
                : "تم إنشاء المنتج بنجاح.";

            elements.productFormMessage.className = (
                "form-message success"
            );

            const savedId = isEditing ? editingProductId : (body.product?.id || elements.productIdInput.value);

            await loadProducts(savedId);

            setTimeout(
                () => {
                    closeProductFormDialog();
                },
                700
            );
        } catch (error) {
            elements.productFormMessage.textContent = (
                error.message
            );

            elements.productFormMessage.className = (
                "form-message error"
            );
        } finally {
            elements.createProductButton.disabled = false;
            elements.createProductButton.textContent = (
                originalLabel
            );
        }
    }
);

elements.productSelect.addEventListener(
    "change",
    async () => {
        const productId = elements.productSelect.value;

        elements.selectedProductId.textContent = (
            productId || "—"
        );

        elements.generateButton.disabled = !productId;
        elements.editProductButton.disabled = !productId;

        await loadProductDetails(productId);

        if (productId) {
            setMessage(
                "المنتج جاهز لبدء الإنتاج."
            );
            showReferenceImage(productId);
            await loadLatestManifest(productId);
        } else {
            setMessage(
                "اختر منتجًا لبدء الإنتاج."
            );
            clearImage();
            clearRunResult();
            setBadge("لا توجد نتيجة", "neutral");
        }
    }
);

elements.generateButton.addEventListener(
    "click",
    async () => {
        const productId = elements.productSelect.value;

        if (!productId) {
            return;
        }

        clearImage();
        setBadge("جاري الإنتاج", "neutral");
        setMessage(
            "يتم الآن تحليل المنتج وبناء البرومبت..."
        );
        elements.runStatus.textContent = "running";
        elements.generationStatus.textContent = "—";
        setLoading(true);

        try {
            const { body } = await fetchJson(
                "/generate",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        product_id: productId,
                    }),
                }
            );

            await loadManifest(productId);

            if (body.status === "succeeded") {
                setMessage(
                    "تم إنتاج الإعلان بنجاح.",
                    "success"
                );
            }
        } catch (error) {
            setBadge("فشل التشغيل", "error");
            setMessage(error.message, "error");
            elements.runStatus.textContent = "failed";
        } finally {
            setLoading(false);
        }
    }
);

elements.copyPromptButton.addEventListener(
    "click",
    async () => {
        if (!currentPrompt) {
            return;
        }

        await navigator.clipboard.writeText(
            currentPrompt
        );

        const originalText = (
            elements.copyPromptButton.textContent
        );

        elements.copyPromptButton.textContent = (
            "تم النسخ"
        );

        window.setTimeout(() => {
            elements.copyPromptButton.textContent = (
                originalText
            );
        }, 1400);
    }
);

loadSystemStatus();
loadProducts();