var previewTemplate;
var dropzone;
var dropzonePreviewNode = document.querySelector("#dropzone-preview-list");
var inputMultipleElements;

if (dropzonePreviewNode) {
    previewTemplate = dropzonePreviewNode.parentNode.innerHTML;
    dropzonePreviewNode.parentNode.removeChild(dropzonePreviewNode);

    // Initialize Dropzone
    dropzone = new Dropzone(".dropzone", {
        url: "http://127.0.0.1:8000/upload_json/",
        method: "post",
        previewTemplate: previewTemplate,
        previewsContainer: "#dropzone-preview",
        autoProcessQueue: false // Disable auto processing
    });
}

// Initialize FilePond plugins
FilePond.registerPlugin(
    FilePondPluginFileEncode,
    FilePondPluginFileValidateSize,
    FilePondPluginImageExifOrientation,
    FilePondPluginImagePreview
);

inputMultipleElements = document.querySelectorAll("input.filepond-input-multiple");

if (inputMultipleElements) {
    Array.from(inputMultipleElements).forEach(function (element) {
        FilePond.create(element);
    });
}

// Assume your form has ID 'my-form-id'
var myForm = document.getElementById('my-form-id');
if (myForm) {
    myForm.addEventListener('submit', function(event) {
        event.preventDefault();
        event.stopPropagation();

        if (dropzone && dropzone.files.length > 0) {
            dropzone.processQueue(); // Process the files in Dropzone
        } else {
            this.submit(); // No files to upload, submit the form
        }
    });
}

// Listen to the queue complete event of Dropzone
if (dropzone) {
    dropzone.on("queuecomplete", function() {
        myForm.submit(); // Submit the form when all files are uploaded
    });
}
