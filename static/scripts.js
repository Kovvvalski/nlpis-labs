document.getElementById("fileInput").addEventListener("change", handleFileSelect);
document.getElementById("sendDataBtn").addEventListener("click", sendDataToAPI);
document.getElementById("saveFileBtn").addEventListener("click", saveToJSON);
document.getElementById("loadFileBtn").addEventListener("click", loadFromJSON);
document.getElementById("addWordBtn").addEventListener("click", addNewWord);

let wordsDTO = [];
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
    wordsDTO = data;
    filteredWords = [...wordsDTO];  // Initialize filtered words with the full list
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

    row.appendChild(wordCell);
    row.appendChild(posCell);
    row.appendChild(formsCell);

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
    wordsDTO[index][field] = value;
  } else {
    wordsDTO[index][field] = value;
  }
}

function updateFormKey(index, oldKey, newKey) {
  const word = wordsDTO[index];
  const formValue = word.forms[oldKey];
  delete word.forms[oldKey];
  word.forms[newKey] = formValue;
}

function updateFormValue(index, key, value) {
  wordsDTO[index].forms[key] = value;
}

function removeForm(index, key) {
  delete wordsDTO[index].forms[key];
  populateTable();
}

function addNewForm(index) {
  const newKey = prompt("Enter new form key:");
  if (newKey) {
    wordsDTO[index].forms[newKey] = "";
    populateTable();
  }
}

function editBaseWord(index) {
  const newBase = prompt("Edit word base:", wordsDTO[index].base);
  if (newBase !== null) {
    wordsDTO[index].base = newBase;
    populateTable();
  }
}

function addNewWord() {
  const newBase = prompt("Enter base word:");
  const newPos = prompt("Enter part of speech:");
  const newForms = {};  // Empty forms object

  if (newBase && newPos) {
    const newWord = {
      base: newBase,
      part_of_speech: newPos,
      forms: newForms
    };
    wordsDTO.push(newWord);
    filteredWords.push(newWord);  // Add to the filtered list as well
    populateTable();
  }
}

function filterTable() {
  const baseWordFilter = document.getElementById("baseWordFilter").value.toLowerCase();
  const posFilter = Array.from(document.getElementById("posFilter").selectedOptions).map(option => option.value);

  filteredWords = wordsDTO.filter(word => {
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
  const blob = new Blob([JSON.stringify(filteredWords, null, 2)], { type: "application/json" });
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
      reader.onload = function (e) {
        wordsDTO = JSON.parse(e.target.result);
        filteredWords = [...wordsDTO];  // Initialize filtered words with the full list
        populateTable();
      };
      reader.readAsText(file);
    }
  });

  input.click();
}
