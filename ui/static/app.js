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

    elements.detailProduct.textContent = (
        productId || "—"
    );

    elements.detailScene.textContent = (
        designDna.scene || "—"
    );

    elements.detailMaterial.textContent = (
        decision.material?.primary || "—"
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
        clearImage();
        setBadge("لا توجد صورة", "error");
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
        `/outputs/${encodeURIComponent(productId)}`
        + "/manifest.json"
    );

    const { response, body } = await fetchJson(url);

    if (!response.ok) {
        throw new Error(
            body.detail || "تعذر تحميل manifest."
        );
    }

    renderManifest(body);
}

async function loadSystemStatus() {
    try {
        const { response, body } = await fetchJson("/");

        if (!response.ok) {
            throw new Error("System unavailable");
        }

        elements.systemDot.classList.add("online");
        elements.systemStatus.textContent = (
            `${body.system} — متصل`
        );
    } catch (error) {
        elements.systemDot.classList.add("offline");
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
    () => {
        const productId = elements.productSelect.value;

        elements.selectedProductId.textContent = (
            productId || "—"
        );

        elements.generateButton.disabled = !productId;

        if (productId) {
            setMessage(
                "المنتج جاهز لبدء الإنتاج."
            );
        } else {
            setMessage(
                "اختر منتجًا لبدء الإنتاج."
            );
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