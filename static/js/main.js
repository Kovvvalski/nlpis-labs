let processedResult = [];
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
    reader.onload = function(e) {
        const text = e.target.result;
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text })
        })
        .then(res => res.json())
        .then(data => {
            processedResult = data;
            renderResults(data);
        })
        .catch(err => console.error(err));
    };
    reader.readAsText(file);
}

function renderResults(data) {
    const container = document.getElementById("results");
    container.innerHTML = "";

    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const pageItems = data.slice(start, end);

    pageItems.forEach((sentenceObj, sIndexOffset) => {
        const sIndex = start + sIndexOffset;
        const sentenceDiv = document.createElement("div");
        sentenceDiv.className = "sentence";

        const sentenceHeader = document.createElement("h3");
        sentenceHeader.textContent = sentenceObj.sentence;
        sentenceDiv.appendChild(sentenceHeader);

        sentenceObj.words.forEach((wordObj, wIndex) => {
            const wordDiv = document.createElement("div");
            wordDiv.className = "word";

            const label = document.createElement("strong");
            label.textContent = `Word: ${wordObj.word}`;
            wordDiv.appendChild(label);

            const textarea = document.createElement("textarea");
            textarea.value = wordObj.predicates.join("\n");

            adjustTextareaHeight(textarea);

            textarea.addEventListener("input", () => {
                adjustTextareaHeight(textarea);
                processedResult[sIndex].words[wIndex].predicates = textarea.value.split("\n");
            });

            wordDiv.appendChild(textarea);
            sentenceDiv.appendChild(wordDiv);
        });

        container.appendChild(sentenceDiv);
    });
    renderPaginationControls();
}

function renderPaginationControls() {
    const container = document.getElementById("results");
    const nav = document.createElement("div");
    nav.className = "pagination";

    const totalPages = Math.ceil(processedResult.length / itemsPerPage);

    const prev = document.createElement("button");
    prev.textContent = "← Previous";
    prev.disabled = currentPage === 1;
    prev.onclick = () => {
        currentPage--;
        renderResults(processedResult);
    };

    const next = document.createElement("button");
    next.textContent = "Next →";
    next.disabled = currentPage === totalPages;
    next.onclick = () => {
        currentPage++;
        renderResults(processedResult);
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


function downloadJSON() {
    const blob = new Blob([JSON.stringify(processedResult, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.download = "semantic_analysis_result.json";
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
