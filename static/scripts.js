document.getElementById("fileInput").addEventListener("change", handleFileSelect);
document.getElementById("sendDataBtn").addEventListener("click", sendDataToAPI);
document.getElementById("saveFileBtn").addEventListener("click", saveToJSON);
document.getElementById("loadFileBtn").addEventListener("click", loadFromJSON);
document.getElementById("addWordBtn").addEventListener("click", addNewWord);

let allWords = [];
let filteredWords = [];  // Store the filtered words for display

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
        const text = e.target.result;
        const fileFormat = file.name.endsWith(".txt") ? "txt" : "rtf"; // Determine format
        extractTextAndSend(text, fileFormat);
    };

    if (file.name.endsWith(".txt")) {
        reader.readAsText(file);
    } else if (file.name.endsWith(".rtf")) {
        reader.readAsText(file);
    }
}

function extractTextAndSend(text, format) {
    // Send the text to the API after extracting
    document.getElementById("sendDataBtn").disabled = false;

    // Prepare request data with format flag
    const requestData = {
        text: text,
        format: format // Include format (txt/rtf)
    };

    fetch("/api/process-text", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
    })
        .then(response => response.json())
        .then(data => {
            allWords = data;
            filteredWords = [...allWords];  // Initialize filtered words with the full list
            populateTable();
            document.getElementById("saveFileBtn").disabled = false;
            document.getElementById("loadFileBtn").disabled = false;
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

function populateTable() {
    const tableBody = document.querySelector("#wordTable tbody");
    tableBody.innerHTML = ""; // Clear existing rows

    // Сортируем слова по алфавиту по свойству "base"
    filteredWords.sort((a, b) => {
        const baseA = a.base.toLowerCase();
        const baseB = b.base.toLowerCase();

        if (baseA < baseB) {
            return -1;
        }
        if (baseA > baseB) {
            return 1;
        }
        return 0; // если слова одинаковые
    });

    filteredWords.forEach((word, index) => {
        const row = document.createElement("tr");

        // Word Cell with editable base
        const wordCell = document.createElement("td");
        wordCell.innerHTML = `<span onclick="editBaseWord(${index})">${word.base}</span>`;

        // Part of Speech Cell with Dropdown
        const posCell = document.createElement("td");
        const posSelector = createPosSelector(word.part_of_speech, index);
        posCell.appendChild(posSelector);

        // Forms Cell
        const formsCell = document.createElement("td");
        formsCell.appendChild(createFormsEditor(word.forms, index));

        // Add Delete button
        const deleteCell = document.createElement("td");
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = () => deleteWord(index);
        deleteCell.appendChild(deleteButton);

        row.appendChild(wordCell);
        row.appendChild(posCell);
        row.appendChild(formsCell);
        row.appendChild(deleteCell);

        tableBody.appendChild(row);
    });
}


function createPosSelector(selectedValue, index) {
    const posOptions = ["Noun", "Verb", "Adjective", "Pronoun", "Preposition", "Conjunction", "Interjection", "Determiner", "Particle"];
    const select = document.createElement("select");

    posOptions.forEach((pos) => {
        const option = document.createElement("option");
        option.value = pos;
        option.textContent = pos;
        if (pos === selectedValue) {
            option.selected = true;
        }
        select.appendChild(option);
    });

    select.addEventListener("change", function () {
        updateWord(index, 'part_of_speech', select.value);
    });

    return select;
}

function createFormsEditor(forms, index) {
    const div = document.createElement("div");

    // Loop through the forms and create input fields for each key-value pair
    Object.keys(forms).forEach((key) => {
        const formPairDiv = document.createElement("div");
        formPairDiv.innerHTML = `
      <input type="text" value="${key}" placeholder="Form Key" onchange="updateFormKey(${index}, '${key}', this.value)" />
      <input type="text" value="${forms[key]}" placeholder="Form Value" onchange="updateFormValue(${index}, '${key}', this.value)" />
      <button onclick="removeForm(${index}, '${key}')">Remove</button>
    `;
        div.appendChild(formPairDiv);
    });

    // Add button for adding new form
    const addFormButton = document.createElement("button");
    addFormButton.textContent = "Add Form";
    addFormButton.addEventListener("click", function () {
        addNewForm(index);
    });

    div.appendChild(addFormButton);

    return div;
}

function updateWord(index, field, value) {
    if (field === "forms") {
        allWords[index][field] = value;
    } else {
        allWords[index][field] = value;
    }
}

function updateFormKey(index, oldKey, newKey) {
    const word = allWords[index];
    const formValue = word.forms[oldKey];
    delete word.forms[oldKey];
    word.forms[newKey] = formValue;
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

    // Создание селектора для выбора части речи
    const posSelector = createPosSelector("", 0);  // Здесь создается селектор без выбранной части речи
    const posDropdown = document.createElement("div");
    posDropdown.appendChild(posSelector);

    // Появляется модальное окно с полем для ввода base и отображением селектора для части речи
    const newPos = posSelector.value;  // Получаем выбранное значение части речи сразу

    const newForms = {};  // Пустой объект для форм

    if (newBase && newPos) {
        const newWord = {
            base: newBase,
            part_of_speech: newPos,
            forms: newForms
        };
        allWords.push(newWord);
        filteredWords.push(newWord);  // Добавляем слово в список фильтрации
        populateTable();
    }
}


function deleteWord(index) {
    allWords.splice(index, 1);
    filteredWords = [...allWords]; // Update filtered words
    populateTable();  // Re-populate table after removal
}

function filterTable() {
    const baseWordFilter = document.getElementById("baseWordFilter").value.toLowerCase();
    const posFilter = Array.from(document.getElementById("posFilter").selectedOptions).map(option => option.value);

    filteredWords = allWords.filter(word => {
        const matchesBase = word.base.toLowerCase().includes(baseWordFilter);
        const matchesPos = posFilter.length === 0 || posFilter.includes(word.part_of_speech);
        return matchesBase && matchesPos;
    });

    populateTable();
}

function sendDataToAPI() {
    alert("Data sent to API successfully!");
}

function saveToJSON() {
    const blob = new Blob([JSON.stringify(filteredWords, null, 2)], {type: "application/json"});
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "words.json";
    link.click();
}

function clearFilters() {
    document.getElementById("baseWordFilter").value = "";

    const posFilter = document.getElementById("posFilter");
    for (let option of posFilter.options) {
        option.selected = false;
    }

    filteredWords = [...allWords]
    populateTable();
}

function loadFromJSON() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";

    input.addEventListener("change", function () {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                allWords = JSON.parse(e.target.result);
                filteredWords = [...allWords];  // Initialize filtered words with the full list
                populateTable();
            };
            reader.readAsText(file);
        }
    });

    input.click();
}
