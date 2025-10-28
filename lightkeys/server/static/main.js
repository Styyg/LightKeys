// ===============================
// 🎹 LightKeys Control Panel
// ===============================

let activeColorMode = null;
let activeEffects = []; // ordre important

// -------------------------------
// Initialisation
// -------------------------------
window.addEventListener("DOMContentLoaded", () => {
    loadSchema();
});

// -------------------------------
// Chargement du schema
// -------------------------------
async function loadSchema() {
    try {
        const res = await fetch("/leds/schema");
        const schema = await res.json();
        buildColorModes(schema.color_modes);
        buildEffectModes(schema.effect_modes);
    } catch (err) {
        console.error("Erreur de chargement du schéma :", err);
    }
}

// -------------------------------
// 🎨 COLOR MODES (exclusif)
// -------------------------------
function buildColorModes(colorModes) {
    const container = document.getElementById("colorModeSelector");
    container.innerHTML = "";

    for (const [name, data] of Object.entries(colorModes)) {
        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = "colorMode";
        radio.value = name;
        radio.id = `colorMode_${name}`;
        radio.onchange = () => selectColorMode(name, data);

        const label = document.createElement("label");
        label.htmlFor = radio.id;
        label.textContent = name;

        container.appendChild(radio);
        container.appendChild(label);
        container.appendChild(document.createElement("br"));
    }
}

function selectColorMode(name, data) {
    activeColorMode = name;

    const paramsContainer = document.getElementById("colorModeParams");
    paramsContainer.innerHTML = "";

    const title = document.createElement("h3");
    title.textContent = name;
    const desc = document.createElement("p");
    desc.textContent = data.description || "";

    paramsContainer.appendChild(title);
    paramsContainer.appendChild(desc);

    const paramsForm = buildParamsForm(data.params);
    paramsContainer.appendChild(paramsForm);

    const btn = document.createElement("button");
    btn.textContent = "Activer ce mode";
    btn.onclick = () => applyColorMode(name, paramsForm);
    paramsContainer.appendChild(btn);
}

async function applyColorMode(name, form) {
    const params = getFormParams(form);

    await fetch("/leds/color_mode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: name }),
    });

    await fetch("/leds/color_params", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ params }),
    });

    alert(`🎨 Mode ${name} activé !`);
}

// -------------------------------
// ✨ EFFECT MODES (cumulatifs + ordonnables)
// -------------------------------
function buildEffectModes(effectModes) {
    const container = document.getElementById("effectModesList");
    container.innerHTML = "";
    enableDrop(container); // active le drag & drop global

    for (const [name, data] of Object.entries(effectModes)) {
        const card = document.createElement("div");
        card.className = "effect-card";
        card.id = `effect_${name}`;
        card.dataset.name = name;

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.onchange = () => toggleEffect(name, data, checkbox.checked);

        const label = document.createElement("label");
        label.textContent = name;

        card.appendChild(checkbox);
        card.appendChild(label);

        makeEffectDraggable(card, name);
        container.appendChild(card);
    }
}

function toggleEffect(name, data, enabled) {
    const card = document.getElementById(`effect_${name}`);

    if (enabled) {
        const form = buildParamsForm(data.params);
        form.classList.add("effect-form");
        card.appendChild(form);

        activeEffects.push(name);
    } else {
        card.querySelectorAll(".effect-form").forEach(el => el.remove());
        activeEffects = activeEffects.filter(e => e !== name);
    }
}

// -------------------------------
// 🔁 Application globale des effets
// -------------------------------
document.getElementById("applyEffects").onclick = async () => {
    const container = document.getElementById("effectModesList");
    refreshEffectOrder(container);

    // Envoi de la liste ordonnée des effets actifs
    await fetch("/leds/effect_modes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ modes: activeEffects }),
    });

    // Envoi des paramètres pour chaque effet actif
    for (const name of activeEffects) {
        const card = document.getElementById(`effect_${name}`);
        const form = card.querySelector(".effect-form");
        if (!form) continue;

        const params = getFormParams(form);
        await fetch("/leds/effect_params", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ params }),
        });
    }

    alert("✨ Effets mis à jour !");
};

// -------------------------------
// ⚙️ Génération dynamique des formulaires
// -------------------------------
function buildParamsForm(paramsSchema) {
    const form = document.createElement("div");
    form.className = "params-form";

    for (const [key, info] of Object.entries(paramsSchema)) {
        const label = document.createElement("label");
        label.textContent = info.label || key;

        let input;

        switch (info.type) {
            case "float":
            case "int":
                input = document.createElement("input");
                input.type = "number";
                input.step = "any";
                if (info.min !== undefined) input.min = info.min;
                if (info.max !== undefined) input.max = info.max;
                break;

            case "color":
                input = document.createElement("input");
                input.type = "color";
                input.value = "#ffffff";
                break;

            case "enum":
                input = document.createElement("select");
                for (const opt of info.options || []) {
                    const option = document.createElement("option");
                    option.value = opt;
                    option.textContent = opt;
                    input.appendChild(option);
                }
                break;

            default:
                input = document.createElement("input");
                input.type = "text";
        }

        input.id = key;
        form.appendChild(label);
        form.appendChild(input);
    }

    return form;
}

function getFormParams(form) {
    const params = {};
    const inputs = form.querySelectorAll("input, select");

    inputs.forEach(input => {
        const key = input.id;
        if (input.type === "number") params[key] = parseFloat(input.value);
        else params[key] = input.value;
    });

    return params;
}

// -------------------------------
// 🧲 Drag & Drop (ordre des effets)
// -------------------------------
function makeEffectDraggable(element, effectName) {
    element.draggable = true;
    element.ondragstart = e => {
        element.classList.add("dragging");
        e.dataTransfer.setData("effect", effectName);
    };
    element.ondragend = () => element.classList.remove("dragging");
}

function enableDrop(container) {
    container.ondragover = e => e.preventDefault();

    container.ondrop = e => {
        e.preventDefault();
        const draggedName = e.dataTransfer.getData("effect");
        const dragged = document.getElementById(`effect_${draggedName}`);
        const target = e.target.closest(".effect-card");

        if (dragged && target && dragged !== target) {
            container.insertBefore(dragged, target);
            refreshEffectOrder(container);
        }
    };
}

function refreshEffectOrder(container) {
    activeEffects = Array.from(container.children)
        .filter(c => c.querySelector("input[type='checkbox']").checked)
        .map(c => c.dataset.name);

    console.log("Nouvel ordre :", activeEffects);
}
