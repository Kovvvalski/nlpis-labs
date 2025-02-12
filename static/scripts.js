document.getElementById("fileInput").addEventListener("change", handleFileSelect);
document.getElementById("saveFileBtn").addEventListener("click", saveToJSON);
document.getElementById("loadFileBtn").addEventListener("click", loadFromJSON);
document.getElementById("addWordBtn").addEventListener("click", addNewWord);

let shownWords = [];
let initialWords = [];
let currentPage = 0;
const ROWS_PER_PAGE = 5;


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
    fetch("/api/process-text", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text, format})
    })
        .then(response => response.json())
        .then(data => {
            shownWords = data;
            shownWords.sort((a, b) => a.base.localeCompare(b.base));
            initialWords = structuredClone(shownWords);
            populateTable();
        })
        .catch(error => console.error("Error:", error));
}

function populateTable() {
    const tableBody = document.querySelector("#wordTable tbody");
    tableBody.innerHTML = "";
    let startIndex = ROWS_PER_PAGE * currentPage;
    let endIndex = Math.min(startIndex + ROWS_PER_PAGE, shownWords.length);
    for (let index = startIndex; index < endIndex; index++) {
        const word = shownWords[index];
        const row = document.createElement("tr");

        if (word.is_exception) row.classList.add("exception");

        row.innerHTML = `
        <td><span onclick="editBaseWord(${index})">${word.base}</span></td>
        <td></td>
        <td></td>
        <td><button onclick="deleteWord(${index})">Delete</button></td>
        <td>${word.is_exception ? `<button onclick="removeException(${index})">Remove Exception</button>` : ""}</td>
    `;

        row.children[1].appendChild(createPosSelector(word.part_of_speech, index));
        row.children[2].appendChild(createFormsEditor(word.forms, index));
        tableBody.appendChild(row);
    }

    const pageNumberElement = document.getElementById("pageNumber");
    pageNumberElement.textContent = `Page ${currentPage + 1}`;

    document.getElementById("prevPageBtn").disabled = currentPage === 0;
    document.getElementById("nextPageBtn").disabled = currentPage >= Math.floor(shownWords.length / ROWS_PER_PAGE);
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
        const newWord = {base: newBase, part_of_speech: "Noun", forms: {}, is_exception: false};
        shownWords.unshift(newWord);
        populateTable();
    }
}

function deleteWord(index) {
    shownWords.splice(index, 1);
    populateTable();
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
    const blob = new Blob([JSON.stringify(shownWords, null, 2)], {type: "application/json"});
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
                shownWords = JSON.parse(e.target.result);
                populateTable();
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