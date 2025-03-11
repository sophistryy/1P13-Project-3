const notes_list = ["A", "B", "C", "D", "E","A", "B", "C", "D"];
const textbox = document.getElementById("DisplayTextbox");
const beforetextbox = document.getElementById("BeforeTextbox");
const aftertextbox = document.getElementById("AfterTextbox");
const tempoTextbox = document.getElementById("tempoTextbox");
const playBtn = document.getElementById("playBtn");
const slowDownBtn = document.getElementById("slowDownBtn");
const speedUpBtn = document.getElementById("speedUpBtn");
const pauseBtn = document.getElementById("pauseBtn");
const continueBtn = document.getElementById("continueBtn");
const resetBtn = document.getElementById("resetBtn");

const initialDelay = 2000;
let delay = initialDelay;
tempoTextbox.innerText = delay;
let index = 0;
let timeoutId = null; 
let isPaused = false;
function updateTextbox() {
    if (index === notes_list.length-1){
        aftertextbox.innerText = "END";
    }
    else{
        aftertextbox.innerText = notes_list[index+1]
    }
    textbox.innerText = notes_list[index];
    index++;

    if (index < notes_list.length) {
        timeoutId = setTimeout(updateTextbox, delay);
    }
    else{
        playBtn.style.display = "block";
        slowDownBtn.style.display = "block";
        pauseBtn.style.display = "none"; 
    }
}
function increaseDelay() {
    delay += 1000; 
    tempoTextbox.innerText = delay;
}
function decreaseDelay() {
    if (delay > 1000) {
        delay -= 1000;
    }
    else{
        speedUpBtn.disabeled = true;
    }
    tempoTextbox.innerText = delay;
}
function pauseLoop() {
    clearTimeout(timeoutId); 
    isPaused = true;
    pauseBtn.style.display = "none"; 
    continueBtn.style.display = "block"; 
    resetBtn.style.display = "block"; 
}
function continueLoop() {
    isPaused = false;
    continueBtn.style.display = "none"; 
    resetBtn.style.display = "none"; 
    pauseBtn.style.display = "block"; 
    updateTextbox(); 
}
function resetPage(){
    location.reload();
}
function startLoop() {
    index = 0;
    textbox.innerText = "";  
    aftertextbox.innerText = ""; 
    playBtn.style.display = "none";
    slowDownBtn.style.display = "none";
    speedUpBtn.style.display = "none";
    pauseBtn.style.display = "block";   
    tempoTextbox.innerText = delay;
    clearTimeout(timeoutId);
    isPaused = false;
    updateTextbox();
}
