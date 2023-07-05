$(document).ready(function() {
  $('#uploadForm').submit(function(e) {
    e.preventDefault();
    var fileInput = $('#fileInput')[0];
    var file = fileInput.files[0];
    
    // Validate file type
    var allowedExtensions = ['.txt', '.pdf', '.doc', '.docx', '.jpg', '.png'];
    var fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!allowedExtensions.includes(fileExtension)) {
      alert('Invalid file type. Allowed file types are: ' + allowedExtensions.join(', '));
      return;
    }

    // Validate file size (in bytes)
    var maxSize = 20 * 1024 * 1024; // 20MB
    if (file.size > maxSize) {
      alert('File size exceeds the allowed limit of 20MB.');
      return;
    }

    // Display the progress bar during upload
    $('#uploadProgress').show();

    // Perform file upload using AJAX
    var formData = new FormData();
    formData.append('file', file);

    $.ajax({
      url: 'upload', // Replace with the URL to your server-side file upload endpoint
      type: 'POST',
      data: formData,
      contentType: false,
      processData: false,
      xhr: function() {
        var xhr = $.ajaxSettings.xhr();
        if (xhr.upload) {
          xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
              var percent = Math.round((e.loaded / e.total) * 100);
              $('.progress-bar').css('width', percent + '%').attr('aria-valuenow', percent).text(percent + '%');
            }
          }, false);
        }
        return xhr;
      },
      success: function(response) {
        // Assuming the response contains the generated short link
        var shortLink = response.shortLink;

        // Update the progress bar to 100%
        $('.progress-bar').css('width', '100%').attr('aria-valuenow', 100).text('100%');

        // Hide the progress bar and display the short link
        $('#uploadProgress').hide();
        $('#shortLinkResult').show();
        $('#shortLink').text(shortLink);
        $('#shortLink').attr('href', shortLink);

        // Provide download link for the uploaded file
        var downloadLink = response.downloadLink;
        var downloadButton = $('<a>')
          .text('Download File')
          .attr('href', downloadLink)
          .attr('download', file.name)
          .addClass('btn btn-primary mt-3');
        $('#shortLinkResult').append(downloadButton);

        // Add event listener for the delete button
        $('#deleteButton').click(function() {
          // Perform the delete logic here
          // You can use AJAX or a library like axios to send a request to the server to delete the file
          $.ajax({
            url: 'delete', // Replace with the URL to your server-side file delete endpoint
            type: 'POST',
            data: { shortLink: shortLink }, // Pass the short link to identify the file to delete
            success: function() {
              // Once the file is successfully deleted, hide the short link and show a success message
              $('#shortLinkResult').hide();
              alert('File deleted successfully.');
            },
            error: function() {
              alert('An error occurred during file deletion. Please try again later.');
            }
          });
        });
      },
      error: function() {
        alert('An error occurred during file upload. Please try again later.');
      }
    });
  });
});
  