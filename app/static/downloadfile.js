function downloadTextFile(postIndex) {
    const textContent = document.getElementById("full-post-content-" + postIndex).innerText;

    const blob = new Blob([textContent], { type: 'text/plain' });

    const a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob);

    const fileName = 'user_input.txt';
    a.download = fileName;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    window.URL.revokeObjectURL(a.href);
  }
