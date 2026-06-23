const logPanel = document.getElementById('log-panel');
function log(message) {
    const time = new Date().toLocaleTimeString();
    logPanel.innerText += `[${time}] ${message}\n`;
    logPanel.scrollTop = logPanel.scrollHeight;
}
function clearLog() {
    logPanel.innerText = '';
}