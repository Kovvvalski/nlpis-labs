document.getElementById("fileInput").addEventListener("change", handleFileSelect);
document.getElementById("saveFileBtn").addEventListener("click", saveToJSON);
document.getElementById("loadFileBtn").addEventListener("click", loadFromJSON);
document.getElementById("addWordBtn").addEventListener("click", addNewWord);
document.getElementById("useContextCheckbox").addEventListener("change", toggleRepeatColumn);
document.getElementById("useContextCheckbox").addEventListener("change", function() {
    const isChecked = this.checked;
    document.getElementById("reloadContextBtn").classList.toggle("use-context-visible", isChecked);
    document.getElementById("contextSearchBtn").classList.toggle("use-context-visible", isChecked);
});
document.getElementById("reloadContextBtn").addEventListener("click", handleReloadContext);
document.getElementById("closeContextSearchBtn").addEventListener("click", () => {
    document.getElementById("contextSearchModal").style.display = "none";
});

// Add new functions
function showContextSearch() {
    document.getElementById("contextSearchModal").style.display = "flex";
    document.getElementById("contextSearchInput").value = "";
    document.getElementById("contextResults").innerHTML = "";
}

let shownWords = [];
let initialWords = [];
let currentPage = 0;
const ROWS_PER_PAGE = 5;

async function searchContext() {
    const phrase = document.getElementById("contextSearchInput").value.trim();
    if (!phrase) return;

    try {
        const response = await fetch("/api/find-context", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ phrase })
        });
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const results = await response.json();
        
        const resultsContainer = document.getElementById("contextResults");
        resultsContainer.innerHTML = "";
        
        if (results.length === 0) {
            resultsContainer.innerHTML = "<div class='no-results'>No matching contexts found</div>";
            return;
        }

        results.forEach(result => {
            const div = document.createElement("div");
            div.className = "context-result";
            div.innerHTML = `
                <div class="context-text">${result.found_context}</div>
                <div class="source-file">Source: ${result.source_file.split('/').pop()}</div>
            `;
            resultsContainer.appendChild(div);
        });
    } catch (error) {
        console.error("Context search failed:", error);
        alert("Search failed: " + error.message);
    }
}

async function handleReloadContext() {
    try {
        const response = await fetch("/api/reload-context");
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        
        const contextWords = await response.json();
        
        // Clear existing context words and add new ones
        shownWords = [
            ...shownWords.filter(word => !word.fromContext),  // Keep non-context words
            ...contextWords.map(word => ({ ...word, fromContext: true }))  // Add fresh context words
        ];
        
        shownWords.sort((a, b) => a.base.localeCompare(b.base));
        currentPage = 0;
        populateTable();
        updateWordCount();
    } catch (error) {
        console.error("Failed to reload context:", error);
        alert("Error reloading context: " + error.message);
    }
}

// New column visibility control
function toggleRepeatColumn() {
    const table = document.getElementById("wordTable");
    table.classList.toggle("show-repeat-count", this.checked);
    populateTable();
}

function updateWordCount() {
    document.getElementById("totalWordsCount").textContent = 
        `Total words: ${shownWords.length}`;
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && (file.name.endsWith(".txt") || file.name.endsWith(".rtf"))) {
        readFile(file);
    } else {
        alert("Please select a valid .txt or .rtf file.");
    }
}

function readFile(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
        extractTextAndSend(e.target.result, file.name.endsWith(".txt") ? "txt" : "rtf");
    };
    reader.readAsText(file);
}

function extractTextAndSend(text, format) {
    const useContext = document.getElementById("useContextCheckbox").checked;
    const context = useContext ? { context: document.getElementById("fileInput").files[0]?.name || "" } : {};

    fetch("/api/process-text", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ text, format, ...context })
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(newWord => {
            // Modified duplicate check: strict comparison for non-context mode
            const existing = shownWords.find(w => 
                useContext ? 
                w.base.toLowerCase() === newWord.base.toLowerCase() :  // Context mode: merge by base
                w.base.toLowerCase() === newWord.base.toLowerCase() &&  // Normal mode: exact match
                w.part_of_speech === newWord.part_of_speech
            );

            if (!existing) {
                if (!useContext) {
                    // For non-context: reset repeat_count and remove context marker
                    newWord.repeat_count = 1;
                    delete newWord.fromContext;
                }
                shownWords.push(newWord);
            } else {
                // Merge logic
                if (!existing.part_of_speech && newWord.part_of_speech) {
                    existing.part_of_speech = newWord.part_of_speech;
                }

                Object.entries(newWord.forms).forEach(([key, value]) => {
                    if (!existing.forms[key]) existing.forms[key] = value;
                });

                if (useContext) {
                    existing.repeat_count = (existing.repeat_count || 0) + (newWord.repeat_count || 1);
                } else {
                    // Non-context mode: preserve manual edits
                    existing.is_exception = newWord.is_exception || existing.is_exception;
                }
            }
        });

        shownWords.sort((a, b) => a.base.localeCompare(b.base));
        initialWords = structuredClone(shownWords);
        populateTable();
        updateWordCount();
    })
    .catch(error => console.error("Error:", error));
}

function populateTable() {
    const tableBody = document.querySelector("#wordTable tbody");
    const useContext = document.getElementById("useContextCheckbox").checked;
    tableBody.innerHTML = "";
    
    const startIndex = currentPage * ROWS_PER_PAGE;
    const endIndex = Math.min(startIndex + ROWS_PER_PAGE, shownWords.length);

    for (let i = startIndex; i < endIndex; i++) {
        const word = shownWords[i];
        const row = document.createElement("tr");

        if (word.is_exception) row.classList.add("exception");

        row.innerHTML = `
        <td><span onclick="editBaseWord(${i})">${word.base}</span></td>
        <td></td>
        <td></td>
        ${useContext ? `<td class="repeat-count">${word.repeat_count || 1}</td>` : ''}
        <td><button onclick="deleteWord(${i})">Delete</button></td>
        ${word.is_exception ? `<td><button onclick="removeException(${i})">Remove Exception</button></td>` : '<td></td>'}
    `;
    
    if (word.fromContext) {
        row.classList.add("context-word");
    }

        row.children[1].appendChild(createPosSelector(word.part_of_speech, i));
        row.children[2].appendChild(createFormsEditor(word.forms, i));
        tableBody.appendChild(row);
    }

    updatePaginationControls();

        if (shownWords.length === 0) {
        currentPage = 0;
        document.getElementById("pageNumber").textContent = "Page 1";
    }
}

function updatePaginationControls() {
    const totalPages = Math.ceil(shownWords.length / ROWS_PER_PAGE);
    document.getElementById("pageNumber").textContent = `Page ${currentPage + 1} of ${totalPages || 1}`;
    document.getElementById("prevPageBtn").disabled = currentPage === 0;
    document.getElementById("nextPageBtn").disabled = currentPage >= totalPages - 1 || totalPages === 0;
}

function changePage(direction) {
    currentPage += direction;
    currentPage = Math.max(0, Math.min(currentPage, Math.floor(shownWords.length / ROWS_PER_PAGE)));
    populateTable();
}

function removeException(index) {
    shownWords[index].is_exception = false;
    populateTable();
}

function markAsException(index) {
    shownWords[index].is_exception = true;
    populateTable();
}

function createPosSelector(selectedValue, index) {
    const select = document.createElement("select");
    ["Noun", "Verb", "Adjective", "Pronoun", "Preposition", "Conjunction", "Interjection", "Determiner", "Particle"].forEach(pos => {
        const option = new Option(pos, pos, pos === selectedValue, pos === selectedValue);
        select.appendChild(option);
    });
    select.addEventListener("change", () => updateWord(index, 'part_of_speech', select.value));
    return select;
}

function createFormsEditor(forms, index) {
    const div = document.createElement("div");
    Object.entries(forms).forEach(([key, value]) => {
        const formDiv = document.createElement("div");
        formDiv.innerHTML = `
            <input type="text" value="${key}" onchange="updateFormKey(${index}, '${key}', this.value)" />
            <input type="text" value="${value}" onchange="updateFormValue(${index}, '${key}', this.value)" />
            <button onclick="removeForm(${index}, '${key}')">Remove</button>
        `;
        div.appendChild(formDiv);
    });
    const addFormButton = document.createElement("button");
    addFormButton.textContent = "Add Form";
    addFormButton.onclick = () => addNewForm(index);
    div.appendChild(addFormButton);
    return div;
}

function updateWord(index, field, value) {
    shownWords[index][field] = value;
}

function updateFormKey(index, oldKey, newKey) {
    const word = shownWords[index];
    word.forms[newKey] = word.forms[oldKey];
    delete word.forms[oldKey];
}

function updateFormValue(index, key, value) {
    shownWords[index].forms[key] = value;
}

function removeForm(index, key) {
    delete shownWords[index].forms[key];
    populateTable();
}

function addNewForm(index) {
    const newKey = prompt("Enter new form key:");
    if (newKey) {
        shownWords[index].forms[newKey] = "";
        populateTable();
    }
}

function editBaseWord(index) {
    const newBase = prompt("Edit word base:", shownWords[index].base);
    if (newBase !== null) {
        shownWords[index].base = newBase;
        populateTable();
    }
}

function addNewWord() {
    const newBase = prompt("Enter base word:");
    if (newBase) {
        const newWord = {
            base: newBase,
            part_of_speech: "Noun",
            forms: {},
            is_exception: false,
            repeat_count: 1
        };
        shownWords.unshift(newWord);
        populateTable();
        updateWordCount();
    }
}

function deleteWord(index) {
    shownWords.splice(index, 1);
    populateTable();
    updateWordCount(); 
}

function filterTable() {
    const baseWordFilter = document.getElementById("baseWordFilter").value.toLowerCase();
    const posFilter = Array.from(document.getElementById("posFilter").selectedOptions).map(option => option.value);
    shownWords = shownWords.filter(word => word.base.toLowerCase().includes(baseWordFilter) && (posFilter.length === 0 || posFilter.includes(word.part_of_speech)));
    shownWords.sort((a, b) => a.base.localeCompare(b.base));
    currentPage = 0;
    populateTable();
}

function saveToJSON() {
    const data = shownWords.map(word => ({
        ...word,
        repeat_count: word.repeat_count || 1
    }));
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "words.json";
    link.click();
}

function loadFromJSON() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";
    input.addEventListener("change", function () {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                shownWords = JSON.parse(e.target.result).map(word => ({
                    ...word,
                    repeat_count: word.repeat_count || 1
                }));
                populateTable();
                updateWordCount();
            };
            reader.readAsText(file);
        }
    });
    input.click();
}

function reset() {
    shownWords = structuredClone(initialWords);
    currentPage = 0;
    populateTable();
    updateWordCount(); 
}

function helpMe() {
    const helpModal = document.getElementById("helpModal");
    helpModal.style.display = "flex";
}

document.getElementById("closeHelpBtn").addEventListener("click", function () {
    const helpModal = document.getElementById("helpModal");
    helpModal.style.display = "none";
});

window.addEventListener("click", function (event) {
    const helpModal = document.getElementById("helpModal");
    if (event.target === helpModal) {
        helpModal.style.display = "none";
    }
});