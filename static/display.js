const notes_list = ["A", "B", "C", "D", "E"];
// Accessing all elements that must be used
const textbox = document.getElementById("DisplayTextbox");
const beforetextbox = document.getElementById("BeforeTextbox");
const aftertextbox = document.getElementById("AfterTextbox");
const tempoTextbox = document.getElementById("tempoTextbox");
const playBtn = document.getElementById("playBtn");
const pauseBtn = document.getElementById("pauseBtn");
const continueBtn = document.getElementById("continueBtn");
const resetBtn = document.getElementById("resetBtn");


const initialDelay = 2000;
let delay = initialDelay;
tempoTextbox.innerText = delay/1000;
let index = 0;
let timeoutId = null; 
let isPaused = false;

function updateTextbox() {
    // Display note of current index and next index. Increase index value, set timeout to exectue next display after specificed delay. 
    textbox.innerText = notes_list[index];

    if (index === notes_list.length-1){
        aftertextbox.innerText = "END";
    }
    else{
        aftertextbox.innerText = notes_list[index+1]
    }

    index++;

    if (index < notes_list.length) {
        timeoutId = setTimeout(updateTextbox, delay);
    }
    else{
        // When loop is over, option to replay is presented
        playBtn.style.display = "block";
        slowDownBtn.disabled = false;
        speedUpBtn.disabled = false;
        pauseBtn.style.display = "none"; 
    }
}
function increaseDelay() {
    // if(delay>1000){
    //     speedUpBtn.disabled= false;
    // }
    delay += 1000; 
    tempoTextbox.innerText = delay/1000;
}
function decreaseDelay() {
    // Does not allow delay between notes to go below 1 second
    if (delay > 1000) {
        delay -= 1000;
    }
    // else{
    //     speedUpBtn.disabled = true;
    // }
    tempoTextbox.innerText = delay/1000;
}
function pauseLoop() {
    // Clears current loop. Shows option to continue or reset. Enables tempo change and rewind/forward. 
    clearTimeout(timeoutId); 
    isPaused = true;
    pauseBtn.style.display = "none"; 
    continueBtn.style.display = "block"; 
    resetBtn.style.display = "block";
    slowDownBtn.disabled= false;
    speedUpBtn.disabled = false; 
    backBtn.disabled = false;
    forwardBtn.disabled = false;
}
function continueLoop() {
    // Redisplays pause button. Disables tempo change and rewind/forward.
    isPaused = false;
    continueBtn.style.display = "none"; 
    resetBtn.style.display = "none"; 
    pauseBtn.style.display = "block"; 
    slowDownBtn.disabled= true;
    speedUpBtn.disabled = true; 
    backBtn.disabled = true;
    forwardBtn.disabled = true;
    index -=1 ;
    updateTextbox(); 
}
function resetPage(){
    location.reload();
}
function rewind(){
    // Rewinding is enabled as long as song is not at begenning.
    if (isPaused && index> 1){
        aftertextbox.innerText = notes_list[index-1]
        textbox.innerText = notes_list[index-2];
        index -=1
    }
}
function forward(){
    // Can only increase index if index is not already at max index
    if (isPaused && index < notes_list.length-1){
        textbox.innerText = notes_list[index];
        if (index === notes_list.length-1){
            aftertextbox.innerText = "END";
        }
        else{
            aftertextbox.innerText = notes_list[index+1]
        }
        index +=1
    }

}
function startLoop() {
    // Resets index. Clears textbox. Only displays pause button. 
    index = 0;
    textbox.innerText = "";  
    aftertextbox.innerText = ""; 
    playBtn.style.display = "none";
    slowDownBtn.disabled= true;
    speedUpBtn.disabled = true;
    pauseBtn.style.display = "block";   
    tempoTextbox.innerText = delay/1000;
    clearTimeout(timeoutId);
    isPaused = false;
    updateTextbox();
}
