function runCode() {
    let htmlContent = document.getElementById("submission-form").elements["html"].value;
    let cssContent = document.getElementById("submission-form").elements["css"].value;

    let output = document.getElementById("output-frame").contentDocument;
    console.log("Test content\n", '<html><head><style>' + cssContent + '</style></head><body>' + htmlContent + '</body></html>');
    output.open();
    output.write('<html><head><style>' + cssContent + '</style></head><body>' + htmlContent + '</body></html>');
    output.close();

    console.log(output.body.innerHTML);
}