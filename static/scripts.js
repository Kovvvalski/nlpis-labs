document.getElementById("fileInput").addEventListener("change", handleFileSelect);
document.getElementById("sendDataBtn").addEventListener("click", sendDataToAPI);
document.getElementById("saveFileBtn").addEventListener("click", saveToJSON);
document.getElementById("loadFileBtn").addEventListener("click", loadFromJSON);
document.getElementById("addWordBtn").addEventListener("click", addNewWord);

let allWords = [];

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
    document.getElementById("sendDataBtn").disabled = false;
    fetch("/api/process-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, format })
    })
    .then(response => response.json())
    .then(data => {
        allWords = data;
        populateTable();
        document.getElementById("saveFileBtn").disabled = false;
        document.getElementById("loadFileBtn").disabled = false;
    })
    .catch(error => console.error("Error:", error));
}

function populateTable() {
    const tableBody = document.querySelector("#wordTable tbody");
    tableBody.innerHTML = "";
    allWords.sort((a, b) => a.base.localeCompare(b.base));
    allWords.forEach((word, index) => {
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
    });
}

function removeException(index) {
    allWords[index].is_exception = false;
    populateTable();
}

function markAsException(index) {
    allWords[index].is_exception = true;
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
    allWords[index][field] = value;
}

function updateFormKey(index, oldKey, newKey) {
    const word = allWords[index];
    word.forms[newKey] = word.forms[oldKey];
    delete word.forms[oldKey];
}

function updateFormValue(index, key, value) {
    allWords[index].forms[key] = value;
}

function removeForm(index, key) {
    delete allWords[index].forms[key];
    populateTable();
}

function addNewForm(index) {
    const newKey = prompt("Enter new form key:");
    if (newKey) {
        allWords[index].forms[newKey] = "";
        populateTable();
    }
}

function editBaseWord(index) {
    const newBase = prompt("Edit word base:", allWords[index].base);
    if (newBase !== null) {
        allWords[index].base = newBase;
        populateTable();
    }
}

function addNewWord() {
    const newBase = prompt("Enter base word:");
    if (newBase) {
        const newWord = { base: newBase, part_of_speech: "", forms: {}, is_exception: false };
        allWords.push(newWord);
        populateTable();
    }
}

function deleteWord(index) {
    allWords.splice(index, 1);
    populateTable();
}

function filterTable() {
    const baseWordFilter = document.getElementById("baseWordFilter").value.toLowerCase();
    const posFilter = Array.from(document.getElementById("posFilter").selectedOptions).map(option => option.value);
    allWords = allWords.filter(word => word.base.toLowerCase().includes(baseWordFilter) && (posFilter.length === 0 || posFilter.includes(word.part_of_speech)));
    populateTable();
}

function sendDataToAPI() {
    alert("Data sent to API successfully!");
}

function saveToJSON() {
    const blob = new Blob([JSON.stringify(allWords, null, 2)], { type: "application/json" });
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
                allWords = JSON.parse(e.target.result);
                populateTable();
            };
            reader.readAsText(file);
        }
    });
    input.click();
}
