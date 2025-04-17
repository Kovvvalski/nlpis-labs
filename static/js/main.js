let processedXML = "";
let currentPage = 1;
const itemsPerPage = 5;

function analyzeText() {
    const fileInput = document.getElementById("fileInput");
    if (!fileInput.files.length) {
        alert("Please select a .txt file.");
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        const text = e.target.result;
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({text})
        })
            .then(res => res.text())
            .then(xmlText => {
                processedXML = xmlText;
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(xmlText, "application/xml");
                renderResults(xmlDoc);
            })
            .catch(err => console.error(err));
    };
    reader.readAsText(file);
}

function renderResults(xmlDoc) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    const sentences = Array.from(xmlDoc.getElementsByTagName("sentence"));
    const totalPages = Math.ceil(sentences.length / itemsPerPage);
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageItems = sentences.slice(start, end);

    pageItems.forEach(sentenceElem => {
        const sentenceDiv = document.createElement("div");
        sentenceDiv.className = "sentence";

        const header = document.createElement("h3");
        header.textContent = sentenceElem.getAttribute("text");
        sentenceDiv.appendChild(header);

        const words = sentenceElem.getElementsByTagName("word");
        Array.from(words).forEach(wordElem => {
            const wordDiv = document.createElement("div");
            wordDiv.className = "word";

            const label = document.createElement("strong");
            label.textContent = `Word: ${wordElem.getAttribute("text")}`;
            wordDiv.appendChild(label);
            ["synonyms", "definitions", "hypernyms"].forEach(type => {
                const groupDiv = document.createElement("div");
                groupDiv.className = "group";

                const sectionLabel = document.createElement("div");
                sectionLabel.innerHTML = `<em>${type.charAt(0).toUpperCase() + type.slice(1)}:</em>`;

                const textarea = document.createElement("textarea");
                const items = wordElem.getElementsByTagName(type)[0]?.getElementsByTagName("item");
                textarea.value = Array.from(items || []).map(i => i.textContent).join("\n");
                adjustTextareaHeight(textarea);

                groupDiv.appendChild(sectionLabel);
                groupDiv.appendChild(textarea);
                wordDiv.appendChild(groupDiv);
            });

            sentenceDiv.appendChild(wordDiv);
        });

        container.appendChild(sentenceDiv);
    });

    renderPaginationControls(sentences.length);
}

function renderPaginationControls(totalItems) {
    const container = document.getElementById("results");
    const nav = document.createElement("div");
    nav.className = "pagination";

    const totalPages = Math.ceil(totalItems / itemsPerPage);

    const prev = document.createElement("button");
    prev.textContent = "← Previous";
    prev.disabled = currentPage === 1;
    prev.onclick = () => {
        currentPage--;
        analyzeText(); // re-fetch or re-render
    };

    const next = document.createElement("button");
    next.textContent = "Next →";
    next.disabled = currentPage === totalPages;
    next.onclick = () => {
        currentPage++;
        analyzeText();
    };

    const pageInfo = document.createElement("span");
    pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    pageInfo.style.margin = "0 10px";

    nav.appendChild(prev);
    nav.appendChild(pageInfo);
    nav.appendChild(next);
    container.appendChild(nav);
}

function adjustTextareaHeight(textarea) {
    textarea.style.height = "auto";
    const lineHeight = 20;
    const lines = textarea.value.split("\n").length;
    textarea.style.height = (lines * lineHeight + 10) + "px";
}

function download() {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(processedXML, "application/xml");

    const sentenceElems = Array.from(xmlDoc.getElementsByTagName("sentence"));
    let wordTextareas = document.querySelectorAll("#results .word");

    wordTextareas.forEach((wordDiv, wIndex) => {
        const sentenceIndex = Math.floor(wIndex / itemsPerPage) + (currentPage - 1);
        const sentenceElem = sentenceElems[sentenceIndex];
        const wordElem = sentenceElem.getElementsByTagName("word")[wIndex % itemsPerPage];

        if (!wordElem) return;

        const groupDivs = wordDiv.querySelectorAll(".group");

        ["synonyms", "definitions", "hypernyms"].forEach((type, i) => {
            const textarea = groupDivs[i].querySelector("textarea");
            const newValues = textarea.value.split("\n").map(v => v.trim()).filter(Boolean);

            // Clear existing items
            const container = wordElem.getElementsByTagName(type)[0];
            while (container.firstChild) {
                container.removeChild(container.firstChild);
            }

            // Add updated items
            newValues.forEach(val => {
                const item = xmlDoc.createElement("item");
                item.textContent = val;
                container.appendChild(item);
            });
        });
    });

    const serializer = new XMLSerializer();
    const updatedXML = serializer.serializeToString(xmlDoc);

    const blob = new Blob([updatedXML], {type: "application/xml"});
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.download = "semantic_analysis_result.xml";
    link.href = url;
    link.click();

    URL.revokeObjectURL(url);
}


function openHelp() {
    document.getElementById("helpModal").style.display = "block";
}

function closeHelp() {
    document.getElementById("helpModal").style.display = "none";
}
