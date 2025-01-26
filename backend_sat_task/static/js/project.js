
//     const {
// 	ClassicEditor,
// 	AutoImage,
// 	Autosave,
// 	BlockQuote,
// 	Bold,
// 	CloudServices,
// 	Essentials,
// 	Heading,
// 	ImageBlock,
// 	ImageCaption,
// 	ImageInline,
// 	ImageInsert,
// 	ImageInsertViaUrl,
// 	ImageResize,
// 	ImageStyle,
// 	ImageTextAlternative,
// 	ImageToolbar,
// 	ImageUpload,
// 	Indent,
// 	IndentBlock,
// 	Italic,
// 	Link,
// 	LinkImage,
// 	List,
// 	ListProperties,
// 	MediaEmbed,
// 	Paragraph,
// 	PasteFromOffice,
// 	SimpleUploadAdapter,
// 	SpecialCharacters,
// 	Table,
// 	TableCaption,
// 	TableCellProperties,
// 	TableColumnResize,
// 	TableProperties,
// 	TableToolbar,
// 	TodoList,
// 	Underline
// } = window.CKEDITOR;


// const LICENSE_KEY =
// 	'eyJhbGciOiJFUzI1NiJ9.eyJleHAiOjE3NjkyMTI3OTksImp0aSI6IjVhOGNjNzk5LWNhNWMtNDE2Yi04NTMxLTZkMjUzZjZmZTdkZSIsInVzYWdlRW5kcG9pbnQiOiJodHRwczovL3Byb3h5LWV2ZW50LmNrZWRpdG9yLmNvbSIsImRpc3RyaWJ1dGlvbkNoYW5uZWwiOlsiY2xvdWQiLCJkcnVwYWwiXSwiZmVhdHVyZXMiOlsiRFJVUCJdLCJ2YyI6IjAyYTU2MzcyIn0.PFz4djqRvbgnkz8mdXUak8SNkfcZaUBHWBBWKydWKhpt1Nc2BbZOHKirg3nzdbF_0q8GK0tibdzbGqe6qCWNUA';

// const editorConfig = {
// 	toolbar: {
// 		items: [
// 			'heading',
// 			'|',
// 			'bold',
// 			'italic',
// 			'underline',
// 			'|',
// 			'specialCharacters',
// 			'link',
// 			'insertImage',
// 			'mediaEmbed',
// 			'insertTable',
// 			'blockQuote',
// 			'|',
// 			'bulletedList',
// 			'numberedList',
// 			'todoList',
// 			'outdent',
// 			'indent'
// 		],
// 		shouldNotGroupWhenFull: false
// 	},
// 	plugins: [
// 		AutoImage,
// 		Autosave,
// 		BlockQuote,
// 		Bold,
// 		CloudServices,
// 		Essentials,
// 		Heading,
// 		ImageBlock,
// 		ImageCaption,
// 		ImageInline,
// 		ImageInsert,
// 		ImageInsertViaUrl,
// 		ImageResize,
// 		ImageStyle,
// 		ImageTextAlternative,
// 		ImageToolbar,
// 		ImageUpload,
// 		Indent,
// 		IndentBlock,
// 		Italic,
// 		Link,
// 		LinkImage,
// 		List,
// 		ListProperties,
// 		MediaEmbed,
// 		Paragraph,
// 		PasteFromOffice,
// 		SimpleUploadAdapter,
// 		SpecialCharacters,
// 		Table,
// 		TableCaption,
// 		TableCellProperties,
// 		TableColumnResize,
// 		TableProperties,
// 		TableToolbar,
// 		TodoList,
// 		Underline
// 	],
// 	heading: {
// 		options: [
// 			{
// 				model: 'paragraph',
// 				title: 'Paragraph',
// 				class: 'ck-heading_paragraph'
// 			},
// 			{
// 				model: 'heading1',
// 				view: 'h1',
// 				title: 'Heading 1',
// 				class: 'ck-heading_heading1'
// 			},
// 			{
// 				model: 'heading2',
// 				view: 'h2',
// 				title: 'Heading 2',
// 				class: 'ck-heading_heading2'
// 			},
// 			{
// 				model: 'heading3',
// 				view: 'h3',
// 				title: 'Heading 3',
// 				class: 'ck-heading_heading3'
// 			},
// 			{
// 				model: 'heading4',
// 				view: 'h4',
// 				title: 'Heading 4',
// 				class: 'ck-heading_heading4'
// 			},
// 			{
// 				model: 'heading5',
// 				view: 'h5',
// 				title: 'Heading 5',
// 				class: 'ck-heading_heading5'
// 			},
// 			{
// 				model: 'heading6',
// 				view: 'h6',
// 				title: 'Heading 6',
// 				class: 'ck-heading_heading6'
// 			}
// 		]
// 	},
// 	image: {
// 		toolbar: [
// 			'toggleImageCaption',
// 			'imageTextAlternative',
// 			'|',
// 			'imageStyle:inline',
// 			'imageStyle:wrapText',
// 			'imageStyle:breakText',
// 			'|',
// 			'resizeImage'
// 		]
// 	},
// 	initialData:
// 		`Type or paste your content here!

// 	Note: This WYSISYG is made for html tags, Image Uploading is not yet supported`,
// 	licenseKey: LICENSE_KEY,
// 	link: {
// 		addTargetToExternalLinks: true,
// 		defaultProtocol: 'https://',
// 		decorators: {
// 			toggleDownloadable: {
// 				mode: 'manual',
// 				label: 'Downloadable',
// 				attributes: {
// 					download: 'file'
// 				}
// 			}
// 		}
// 	},
// 	list: {
// 		properties: {
// 			styles: true,
// 			startIndex: true,
// 			reversed: true
// 		}
// 	},
// 	placeholder:`Type or paste your content here!
// 	Note: This WYSISYG is made for html tags, Image Uploading is not yet supported
// 	`,
// 	table: {
// 		contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
// 	}
// };

// // Initialize first editor
// ClassicEditor
//     .create(document.querySelector('#editor'), editorConfig)
//     .then(editor => {
//         editors.set('editor', editor);
//     })
//     .catch(error => {
//         console.error(error);
//     });

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

// Replace CKEditor initialization with UnityRichTextEditor
function initializeEditor(elementId) {
    const editor = new UnityRichTextEditor(elementId);
    editors.set(elementId, editor);
    return editor;
}

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
        imageUrlInput.value =  error;
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



