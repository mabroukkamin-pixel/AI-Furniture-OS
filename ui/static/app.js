const elements = {
    systemDot: document.querySelector("#systemDot"),
    systemStatus: document.querySelector("#systemStatus"),
    productSelect: document.querySelector("#productSelect"),
    selectedProductId: document.querySelector(
        "#selectedProductId"
    ),
    generateButton: document.querySelector(
        "#generateButton"
    ),
    runMessage: document.querySelector("#runMessage"),
    runStatus: document.querySelector("#runStatus"),
    generationStatus: document.querySelector(
        "#generationStatus"
    ),
    auditScore: document.querySelector("#auditScore"),
    promptLength: document.querySelector("#promptLength"),
    previewBadge: document.querySelector("#previewBadge"),
    emptyPreview: document.querySelector("#emptyPreview"),
    generatedImage: document.querySelector(
        "#generatedImage"
    ),
    detailProduct: document.querySelector("#detailProduct"),
    detailSize: document.querySelector("#detailSize"),
    detailPrice: document.querySelector("#detailPrice"),
    detailScene: document.querySelector("#detailScene"),
    detailMaterial: document.querySelector(
        "#detailMaterial"
    ),
    detailEngine: document.querySelector("#detailEngine"),
    artifactList: document.querySelector("#artifactList"),
    promptPreview: document.querySelector("#promptPreview"),
    copyPromptButton: document.querySelector(
        "#copyPromptButton"
    ),
};

let currentPrompt = "";

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
        return;
    }

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

function renderManifest(manifest) {
    const productId = manifest.product_id;
    const run = manifest.run || {};
    const generation = manifest.generation || {};
    const designDna = manifest.design_dna || {};
    const decision = manifest.decision || {};
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

async function loadManifest(productId) {
    const url = (
        `/runs/${encodeURIComponent(productId)}/latest`
    );

    const { response, body } = await fetchJson(url);

    if (!response.ok) {
        throw new Error(
            body.detail || "تعذر تحميل manifest."
        );
    }

    renderManifest(body);
}

async function loadLatestManifest(productId) {
    if (!productId) {
        return;
    }

    try {
        await loadManifest(productId);
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

async function loadProducts() {
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
        } else {
            const preferredProduct = (
                body.products.find(
                    (product) => product.id === "Partition001"
                )
                || body.products[0]
            );

            elements.productSelect.value = preferredProduct.id;
            elements.selectedProductId.textContent = preferredProduct.id;
            elements.generateButton.disabled = false;

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

        setMessage(error.message, "error");
    }
}

elements.productSelect.addEventListener(
    "change",
    async () => {
        const productId = elements.productSelect.value;

        elements.selectedProductId.textContent = (
            productId || "—"
        );

        elements.generateButton.disabled = !productId;

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