function downloadTextFile(postIndex) {
    // Get the user-entered text
    const textContent = document.getElementById("full-post-content-" + postIndex).innerText;
    
    // Create a Blob object containing the text
    const blob = new Blob([textContent], { type: 'text/plain' });

    // Create a temporary anchor element
    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);

    // Set the file name
    const fileName = 'user_input.txt';
    a.download = fileName;

    // Programmatically click the anchor to trigger the download
    document.body.appendChild(a);
    a.click();

    // Clean up
    document.body.removeChild(a);
    window.URL.revokeObjectURL(a.href);
  }
