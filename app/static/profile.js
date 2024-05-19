function downloadTextFile(postIndex) {

  const textContent = document.getElementById("full-post-content-" + postIndex).querySelector("code").innerText;

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

function saveChanges() {

  var htmlContent = document.getElementById("HtmlCode").value;
  var cssContent = document.getElementById("CssCode").value;


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

  document.getElementById('HtmlCode').value = htmlPart;
  document.getElementById('CssCode').value = cssPart;
  document.getElementById('postId').value = postId;

  runCode();

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

function confirmDelete(postId) {

  var confirmation = confirm('Are you sure you want to delete this post?');

  if (confirmation) {
      window.location.href = '/delete?postId=' + postId;
  }
}
