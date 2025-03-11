const notes_list = ["A", "B", "C", "D", "E"];
const textbox = document.getElementById("DisplayTextbox");
const playAgainBtn = document.getElementById("playAgainBtn");
const delay = 2000;
let index = 0; 
function updateTextbox() {
    textbox.value = notes_list[index];
    index++;

    if (index < notes_list.length) {
        setTimeout(updateTextbox, delay);
    }
    else{
        playAgainBtn.style.display = "block";
    }
}
function startLoop() {
    index = 0;
    textbox.value = ""; 
    playAgainBtn.style.display = "none"; 
    updateTextbox();
}
startLoop()