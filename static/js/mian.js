const modal = document.getElementById("help-modal");
const helpBtn = document.getElementById("help-btn");
const closeModal = document.querySelector(".close");
const grammarBox = document.getElementById('grammar-box');

helpBtn.onclick = function () {
    modal.style.display = "block";
}

closeModal.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

function adjustTextareaHeight() {
    grammarBox.style.height = 'auto';
    grammarBox.style.height = grammarBox.scrollHeight + 'px';
}

grammarBox.addEventListener('input', adjustTextareaHeight);

document.getElementById('download-btn').addEventListener('click', () => {
    const content = grammarBox.value;
    if (!content.trim()) {
        alert("Grammar box is empty.");
        return;
    }

    const filename = prompt("Enter filename for grammar (without extension):", "grammar");
    if (filename === null) return;

    const blob = new Blob([content], {type: 'text/plain;charset=utf-8'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename + '.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});

function updateGrammarBox(content) {
    grammarBox.value = content;
    adjustTextareaHeight();
}

document.getElementById('file-upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const reader = new FileReader();
    reader.onload = async function (event) {
        const text = event.target.result;

        const res = await fetch('/parse', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });

        const data = await res.json();

        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';

        updateGrammarBox(data.grammar);
        const sentenceData = data.sentences;

        sentenceData.forEach(item => {
            const sentenceBlock = document.createElement('div');
            sentenceBlock.classList.add('sentence-block');

            const sentence = document.createElement('h3');
            sentence.textContent = item.sentence;

            const treeList = document.createElement('div');
            treeList.classList.add('tree-list');

            if (item.error) {
                const errorMessage = document.createElement('p');
                errorMessage.classList.add('error-message');
                errorMessage.textContent = item.error;
                treeList.appendChild(errorMessage);
            } else {
                item.trees.forEach(tree => {
                    if (tree) {
                        const img = document.createElement('img');
                        img.src = '/' + tree;
                        treeList.appendChild(img);
                    }
                });
            }

            sentenceBlock.appendChild(sentence);
            sentenceBlock.appendChild(treeList);
            resultsDiv.appendChild(sentenceBlock);
        });
    };

    reader.readAsText(file);
});