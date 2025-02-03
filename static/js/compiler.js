function setupEditor(id, mode) {
    return CodeMirror.fromTextArea(document.getElementById(id), {
        mode: mode,
        lineNumbers: true,
        autoCloseTags: true,
        autoCloseBrackets: true
    });
}

let htmlEditor = setupEditor("html_code", "xml");
let cssEditor = setupEditor("css_code", "css");
let jsEditor = setupEditor("js_code", "javascript");

function runCode() {
    let html = htmlEditor.getValue();
    let css = "<style>" + cssEditor.getValue() + "</style>";
    let js = "<script>" + jsEditor.getValue() + "<\/script>";

    let iframe = document.getElementById("output").contentWindow.document;
    iframe.open();
    iframe.write(html + css + js);
    iframe.close();
}