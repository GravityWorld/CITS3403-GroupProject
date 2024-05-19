function downloadTextFile(postIndex) {
    // Get the user-entered text
     const textContent = document.getElementById("full-post-content-" + postIndex).querySelector("code").innerText;
     
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

 function saveChanges() {
 // Get the HTML and CSS content
 var htmlContent = document.getElementById("HtmlCode").value;
 var cssContent = document.getElementById("CssCode").value;

 // Populate the hidden input fields with the HTML and CSS content
 document.getElementById("htmlContent").value = htmlContent;
 document.getElementById("cssContent").value = cssContent;
}


 function runCode() {
 let htmlContent = document.getElementById("HtmlCode").value;
 let cssContent = document.getElementById("CssCode").value;

 let output = document.getElementById("output-frame").contentDocument;

 output.open();
 output.write('<html><head><style>' + cssContent + '</style></head><body>' + htmlContent + '</body></html>');
 output.close();

 console.log(output.body.innerHTML);
}


function openEditModal(index, id) {
 const postElement = document.getElementById("full-post-content-" + index);
 const postId = id

 const textContent = postElement.querySelector("code").innerText;
 

 console.log("Test content\n", textContent);


 var htmlRegex = /<body.*?>([\s\S]*)<\/body>/; 
 var cssRegex = /<style.*?>([\s\S]*)<\/style>/; 

 var htmlMatch = textContent.match(htmlRegex);
 var cssMatch = textContent.match(cssRegex);

 var htmlPart = htmlMatch ? htmlMatch[1] : ''; 
 var cssPart = cssMatch ? cssMatch[1] : ''; 
 
 console.log(htmlPart);
 console.log(cssPart);
 // Set the HTML and CSS parts to the text areas in the modal
 document.getElementById('HtmlCode').value = htmlPart;
 document.getElementById('CssCode').value = cssPart;
 document.getElementById('postId').value = postId;

 runCode();
 // Display the modal
 var modal = document.getElementById('postModal');
 modal.style.display = "block";
}

  
 function closeModal() {
   document.getElementById("postModal").style.display = "none";
 }
 
 window.onclick = function (event) {
   var modal = document.getElementById("postModal");
   if (event.target == modal) {
     closeModal();
   }
 };