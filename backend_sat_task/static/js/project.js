class UnityRichTextEditor {
    constructor(elementId) {
        this.container = document.getElementById(elementId);
        this.setupEditor();
        this.createToolbar();
    }

    setupEditor() {
        // Create a textarea instead of a div
        this.textarea = document.createElement('textarea');
        this.textarea.className = 'textarea textarea-bordered h-24 w-full mt-2';
        this.textarea.rows = 5;
        this.container.appendChild(this.textarea);
    }

    createToolbar() {
        const toolbar = document.createElement('div');
        toolbar.className = 'unity-toolbar flex gap-2 mb-2';

        const buttons = [
            { label: 'B', tag: 'b', tooltip: 'Bold' },
            { label: 'I', tag: 'i', tooltip: 'Italic' },
            { label: 'Color', action: () => this.insertColor() },
            { label: 'Size', action: () => this.insertSize() },
        ];

        buttons.forEach(btn => {
            const button = document.createElement('button');
            button.className = 'btn btn-sm';
            button.id = "cta" + "-" + btn.label;
            button.type = 'button';
            button.textContent = btn.label;
            button.title = btn.tooltip || btn.label;
            if (btn.tag) {
                button.onclick = () => this.wrapSelection(btn.tag);
            } else {
                button.onclick = btn.action;
            }

            toolbar.appendChild(button);
        });

        this.container.insertBefore(toolbar, this.textarea);
    }

    wrapSelection(tag) {
        const { selectionStart, selectionEnd, value } = this.textarea;
        const selectedText = value.slice(selectionStart, selectionEnd);

        if (!selectedText) return;

        const before = value.slice(0, selectionStart);
        const after = value.slice(selectionEnd);
        const wrapped = `<${tag}>${selectedText}</${tag}>`;

        this.textarea.value = before + wrapped + after;

        // Adjust cursor
        const newPos = before.length + wrapped.length;
        this.textarea.setSelectionRange(newPos, newPos);
        this.textarea.focus();
    }

    insertColor() {
        const color = prompt('Enter color (red, blue, green, etc):');
        if (color) {
            this.wrapSelection(`color=${color}`);
        }
    }

    insertSize() {
        const size = prompt('Enter size (12, 14, 16, etc):');
        if (size) {
            this.wrapSelection(`size=${size}`);
        }
    }

    getData() {
        return this.textarea.value;
    }
}

// Store editor instances
let editors = new Map();
let url = new URL(window.location.href)

// Replace CKEditor initialization with UnityRichTextEditor
function initializeEditor(elementId) {
    const editor = new UnityRichTextEditor(elementId);
    editors.set(elementId, editor);
    return editor;
}

// for route /create-question logic
if (url.pathname === "/create-question") {
    // Initialize first editor
    initializeEditor('editor');

    // Initialize a second editor for the solution input
    initializeEditor('solution-editor');

    // Add helper function
    function slugify(str) {
        return str
            .toLowerCase()
            .trim()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_-]+/g, '-')
            .replace(/^-+|-+$/g, '');
    }

    /* For create_question.html
        Adding/Removing of Option Field
    */
    function addOption() {
        const container = document.getElementById('options-container');
        const optionCount = container.children.length + 1;

        const div = document.createElement('div');
        div.className = 'flex gap-2';
        div.innerHTML = `
        <input type="text" placeholder="Option ${optionCount}" class="input input-bordered w-full" name="option[]" required/>
        <button type="button" class="btn btn-ghost btn-circle" onclick="removeOption(this)">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    `;
        container.appendChild(div);
    }

    function removeOption(button) {

        button.parentElement.remove();

    }

    /* For create_question.html
        Adding of step fields
    */
    let stepCount = 1;
    const $container = document.getElementById('steps-container');
    const $addButton = document.getElementById('add-step');
    const $imageUploadInput = document.getElementById('image-upload');

    
    $addButton.addEventListener('click', () => {
        stepCount++;
        const $newStep = document.createElement('fieldset');
        $newStep.style.opacity = '0';
        $newStep.style.transform = "translateY(-20px)"
        $newStep.style.transition = "all 1s ease";
        $newStep.className = 'fieldset w-xs bg-base-200 border border-base-300 p-6 rounded-box mb-4 mt-4';
        $newStep.innerHTML = `
            <label class="form-control w-full">
                <div class="label">
                    <span class="label-text">Title</span>
                </div>
                <input id="title-input-${stepCount}" type="text" placeholder="Type here" class="input input-bordered w-full" name="step_title_${stepCount}" required/>
            </label>
			<label class="form-control w-full">
                  <div class="label">
                    <span class="label-text">Image URL</span>
                  </div>
                  <input type="text" placeholder="Type here" class="input input-bordered w-full" id="image-url-step-input-${stepCount}" type="url"/>
			</label>
            <div class="main-container">
                <div class="label">
                    <span class="label-text">Result</span>
                </div>
				<div id="editor_${stepCount}"></div>
            </div>
        `;
        // Set final state
        requestAnimationFrame(() => {
            $newStep.style.opacity = '1';
            $newStep.style.transform = 'translateY(0)';
        });
        $container.appendChild($newStep);
        initializeEditor(`editor_${stepCount}`);

        // // Initialize CKEditor for new step
        // ClassicEditor
        // 	.create(document.querySelector(`#editor_${stepCount}`), editorConfig)
        // 	.then(editor => {
        // 		editors.set(`editor_${stepCount}`, editor);
        // 	})
        // 	.catch(error => {
        // 		console.error(error);
        // 	});
    });

    /* For create_question.html
        handle api _key
    */
    async function isApiKeyValid(key) {
        try {
            const response = await fetch(`/api/v0/validate-key?api_key=${key}`);
            return response.ok;
        } catch (err) {
            console.error(err);
            return false;
        }
    }

    let apiKey = "";
    const $enterButton = document.getElementById('submit-with-key');

    function closeModal() {
        const modal = document.getElementById('api-key-modal');
        modal.classList.add('hidden'); // hide the modal with Tailwind
        document.body.style.overflow = 'auto';
    }

    $enterButton.addEventListener('click', async (event) => {
        event.preventDefault();
        apiKey = document.getElementById('api-key-input').value;
        const isValidApiKey = await isApiKeyValid(apiKey);
        const msg = document.getElementById('api-key-error');
        if (!apiKey) {
            // if not valid then show ann error
            msg.innerHTML = "This is required!!";
        }
        else if (!isValidApiKey) {
            msg.innerHTML = "Invalid API KEY"
        }
        else {
            closeModal();
        }
    });

    // For create_question.html
    //  handle image uploading
    $imageUploadInput.addEventListener('change', handleImageUpload);
    async function handleImageUpload(event) {
        const file = event.target.files[0];
        const imageUrlInput = document.getElementById('image-url-input');
        imageUrlInput.placeholder = "Loading...."
        // Validate file
        if (!file) return;
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file');
            event.target.value = '';
            return;
        }

        try {
            imageUrlInput.innerHTML = "Loading...."
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`/api/v0/upload-image?api_key=${apiKey}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            });
            console.log(response.body);
            if (!response.ok) throw new Error('Upload failed');

            const data = await response.json();
            imageUrlInput.value = data.url;
        } catch (error) {
            console.error('Upload error:', error);
            alert('Failed to upload image. Please try again.');
            event.target.value = '';
            imageUrlInput.value = error;
        }
    }


    /* For create_question.html
        Making a POST request to /api/v0/questions
    */
    async function handleSubmit(e) {
        e.preventDefault();
        const formEl = e.target;
        const submitButton = formEl.querySelector('button[type="submit"]');
        const questionTextarea = formEl.querySelector('#question-textarea');
        // const solutionTextarea = formEl.querySelector('#solution-textarea');
        const corretAnswerInput = formEl.querySelector('#correct-answer-input')
        const optionsInputs = formEl.querySelectorAll('[name="option[]"]');
        const imageUrlInput = formEl.querySelector('#image-url-input');
        const difficultySelect = formEl.querySelector('#difficulty-select');
        const tagsSelect = formEl.querySelector('#tags-select');
        const stepsContainer = formEl.querySelector('#steps-container');
        const solutionContent = editors.get('solution-editor').getData();

        let steps = [];
        let options = Array.from(optionsInputs).map(input => input.value);


        // Handle steps
        Array.from(stepsContainer.children).forEach((fieldset, index) => {
            if (index === 0) {
                // First step has different ID structure
                const editor = editors.get('editor');
                steps.push({
                    Title: fieldset.querySelector('#title-input').value,
                    Result: editor.getData(),
                    ImageUrl: fieldset.querySelector(`#image-url-step-input`).value || null,
                    StepNumber: index + 1
                });
            } else {
                // Added steps use stepCount-based IDs
                const editor = editors.get(`editor_${index + 1}`);
                steps.push({
                    Title: fieldset.querySelector(`#title-input-${index + 1}`).value,
                    Result: editor.getData(),
                    ImageUrl: fieldset.querySelector(`#image-url-step-input-${index + 1}`).value || null,
                    StepNumber: index + 1
                });
            }
        });

        const payload = {
            Question: questionTextarea.value,
            solution: solutionContent,
            CorrectAnswer: corretAnswerInput.value,
            Options: options,
            Steps: steps,
            ImageUrl: imageUrlInput.value || null,
            Difficulty: difficultySelect.value,
            Tags: [{
                Name: tagsSelect.options[tagsSelect.selectedIndex].text,
                Slug: slugify(tagsSelect.value)
            }]
        };

        // Show loading state

        submitButton.classList.add('loading');
        submitButton.disabled = true;

        try {
            const response = await fetch(`/api/v0/questions?api_key=${apiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(response.status);
            }

            const data = await response.json();
            if (data) {
                alert('Question created successfully!');
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
            }
        } catch (error) {
            console.error(error);
            alert('Error creating question. Please try again.');
        }
    }
}

// For index.html
if (url.pathname === "/") {
    class RichTextParser {
        static parse(text) {
            if (!text) return '';

            // Replace Unity Rich Text tags with HTML
            return text
                // Colors
                .replace(/<color=(\w+)>/g, '<span style="color: $1">')
                .replace(/<color=#([A-Fa-f0-9]+)>/g, '<span style="color: #$1">')
                .replace(/<\/color>/g, '</span>')

                // Basic formatting
                .replace(/<b>/g, '<strong>')
                .replace(/<\/b>/g, '</strong>')
                .replace(/<i>/g, '<em>')
                .replace(/<\/i>/g, '</em>')

                // New lines
                .replace(/\n/g, '<br>');
        }
    }
    class QuestionGame {
        constructor() {
            this.questions = [];
            this.currentIndex = 0;
            this.score = 0;
            this.correctAnswer;
            this.init();


            this.$selectedRadioEl;
            this.$explanationContainer = document.getElementById('explanation-container');
            this.$checkButton = document.getElementById('check-cta');
            this.$checkButton.addEventListener('click', () => {
                this.$selectedRadioEl = document.querySelector('input[name=answer]:checked');
                const selectedAnswer = this.$selectedRadioEl?.value;
                if (selectedAnswer) {
                    const isCorrect = this.checkAnswer(selectedAnswer);
                    const $correctRadioInput = document.querySelector(`input[value="${this.correctAnswer}"]`);
                    const correctAnswerBorderClass = "flex items-center space-x-2 cursor-pointer border-2 border-solid border-green-500 min-w-[200px] min-h-[50px] p-4 rounded";
                    // const wrongAnswerBorderClass = "flex items-center space-x-2 cursor-pointer border-2 border-solid border-red-500 min-w-[200px] min-h-[50px] p-4 rounded";
                    // IF you're wondering why I'm imperatively accessing style properties because something is broken, I can't seem to render the red border.
                    if (isCorrect) {
                        this.score++;
                        this.$selectedRadioEl.parentElement.className = correctAnswerBorderClass;
                        this.$selectedRadioEl.style.backgroundColor = "green";
                    } else {
                        this.$selectedRadioEl.parentElement.style.border = "2px solid red"; // Is Tailwind broken? I can't freaking set the border of this parent element with its class names. 
                        this.$selectedRadioEl.style.backgroundColor = "red";
                        $correctRadioInput.parentElement.className = correctAnswerBorderClass;
                        $correctRadioInput.style.backgroundColor = "green";
                    }

                } else {
                    alert('Please select an answer');
                }
            });
            this.$explanation = document.getElementById('explanation');
            this.$steps = document.getElementById('steps');
            this.$nextButton = document.createElement('button');
            this.$nextButton.textContent = 'Next';
            this.$nextButton.className = 'bg-[#C5BAFF] px-6 py-2 rounded-lg font-semibold hover:bg-[#968CCA] ml-2';
            this.$nextButton.addEventListener('click', () => this.nextQuestion());
        }

        async init() {
            try {
                const response = await fetch('/api/v0/questions');
                const data = await response.json();
                this.questions = data.items;
                this.renderQuestion();
            } catch (error) {
                console.error('Failed to load questions:', error);
            }
        }

        renderQuestion() {
            const letters = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
            const question = this.questions[this.currentIndex];
            this.correctAnswer = question.CorrectAnswer;

            document.getElementById('question-text').innerHTML = RichTextParser.parse(question.Question);

            const optionsContainer = document.querySelector('.grid');
            optionsContainer.innerHTML = question.Options.map((option, index) => `
                <label class="flex items-center space-x-2 cursor-pointer border-2 border-solid min-w-[200px] min-h-[50px] p-4 rounded">
                    <input type="radio" name="answer" value="${option}" class="radio checked:bg-black"  />
                    <span class="text-xs">${letters[index]})</span><span class="font-bold text-4xl">${option}</span>
                </label>
            `).join('');
        }

        checkAnswer(selectedAnswer) {
            const question = this.questions[this.currentIndex];
            const isCorrect = selectedAnswer === question.CorrectAnswer;
            const $radioInputs = document.querySelectorAll('input[type="radio"]');


            // Disable all radio inputs after checking
            $radioInputs.forEach(radio => {
                radio.disabled = true;
                radio.parentElement.classList.add('cursor-not-allowed');
                radio.parentElement.classList.remove('cursor-pointer');
            });
            this.renderExplanation(question.Solution, question.Steps);

            // Show next button after checking answer
            this.$checkButton.parentElement.appendChild(this.$nextButton);
            this.$checkButton.disabled = true;
            this.$checkButton.classList.add('opacity-50', "hidden");

            return isCorrect;
        }

        renderExplanation(solution, steps) {
            this.$explanationContainer.classList.remove('hidden');
            this.$explanation.innerHTML = RichTextParser.parse(solution);
    
            const fallbackImage = "https://d12lqqa1y5u348.cloudfront.net/images/elementor-placeholder-image.webp";
    
            steps.forEach((step, index) => {
                this.$steps.innerHTML += `
                    <div id="step-${index}" class="p-2 my-2">
                        <h3 class="font-semibold">${RichTextParser.parse(step?.Title)}</h3>
                        <img src="${step?.ImageUrl || fallbackImage}" 
                             alt="${step?.Title || 'Step image'}" 
                             class="w-full"
                             onerror="this.onerror=null; this.src='${fallbackImage}';" />
                        <p class="my-4">${RichTextParser.parse(step?.Result)}</p>
                    </div>
                `;
            });
        }

        nextQuestion() {
            // Move to next question
            this.currentIndex++;
            if (this.currentIndex >= this.questions.length) {
                alert("That's it, you've already done all the questions!");
                return;
            }

            // Reset UI state
            this.$explanationContainer.classList.add('hidden');
            this.$explanation.innerHTML = '';
            this.$steps.innerHTML = '';
            this.$nextButton.remove();
            this.$checkButton.disabled = false;
            this.$checkButton.classList.remove('opacity-50');
            this.$checkButton.classList.remove('hidden');

            // Render new question
            this.renderQuestion();
        }

    }
    new QuestionGame();


}
