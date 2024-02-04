// Initialize the CKEditor
ClassicEditor.create(document.querySelector("#ckeditor-classic"))
  .then(function (editor) {
    editor.ui.view.editable.element.style.height = "200px";
  })
  .catch(function (error) {
    console.error(error);
  });

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Dropzone configuration
var dropzonePreviewNode = document.querySelector("#dropzone-preview-list");
var previewTemplate = dropzonePreviewNode.parentNode.innerHTML;
dropzonePreviewNode.parentNode.removeChild(dropzonePreviewNode);

var dropzone = new Dropzone(".dropzone", {
    url: "/upload_json/",
    paramName: "file",
    method: "post",
    previewTemplate: previewTemplate,
    previewsContainer: "#dropzone-preview",
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
    },
    autoProcessQueue: false
});

// Form submission handling
var form = document.querySelector('.needs-validation');
form.addEventListener('submit', function(event) {
  if (!form.checkValidity()) {
    event.preventDefault();
    event.stopPropagation();
    form.classList.add('was-validated');
  } else {
    event.preventDefault(); // Prevent default form submission

    dropzone.on('sending', function(file, xhr, formData) {
      var data = new FormData(form);
      for (var [key, value] of data.entries()) {
        formData.append(key, value);
      }
    });

    dropzone.on('queuecomplete', function() {
      location.reload(); // Refresh the page
    });

    dropzone.processQueue(); // Start processing the queued files
  }
});

// Optional: Add listeners for Dropzone events like "success", "error", etc.
dropzone.on('success', function(file, response) {
  console.log('File uploaded successfully', response);
});

dropzone.on('error', function(file, errorMessage) {
  console.error('Error during file upload:', errorMessage);
});
