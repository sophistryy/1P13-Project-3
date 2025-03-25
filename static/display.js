let msg = new SpeechSynthesisUtterance();
let notes_list = [];

// Accessing all elements that must be used
const textbox = document.getElementById("DisplayTextbox");
const beforetextbox = document.getElementById("BeforeTextbox");
const aftertextbox = document.getElementById("AfterTextbox");
const tempoTextbox = document.getElementById("tempoTextbox");
const playBtn = document.getElementById("playBtn");
const pauseBtn = document.getElementById("pauseBtn");
const continueBtn = document.getElementById("continueBtn");
const resetBtn = document.getElementById("resetBtn");
const volumeOn = document.getElementById("volume-button");

(async () => {
	const url = location.href.split("/");
	const response = await fetch("/get_song/" + url[url.length - 1]);
	const data = await response.json();
	notes_list = data;
})();

// let delay = 2000;
// speed is in notes per minute (same as metronome)
let speed = 30
tempoTextbox.innerText = speed;
let index = 0;
let timeoutId = null; 
let isPaused = false;
let isVolumeOn = true;

volumeOn.addEventListener("click", () => {
	isVolumeOn = !isVolumeOn;
	volumeOn.className = isVolumeOn ? "fa fa-volume-high" : "fa fa-volume-xmark";
});

function updateTextbox() {
	// Display note of current index and next index. Increase index value, set timeout to execute next display after specificed delay.
	textbox.innerText = notes_list[index].toString();
	if (textbox.innerText.length > 4) {
		textbox.style.fontSize = (13 - textbox.innerText.length / 2) + "em";
	} else {
		textbox.style.fontSize = "11em";
	}

	// let boxHTML = "";
	// for (let i = 0; i < notes_list[index].length; i++) {
	// 	boxHTML += `<span>${notes_list[index][i]}</span>`;
	// }
	// textbox.innerHTML = boxHTML;
	
	if (isVolumeOn) {
		msg.text = notes_list[index].toString().toLowerCase();
		window.speechSynthesis.speak(msg);
	}

	if (index === notes_list.length - 1) {
		aftertextbox.innerText = "END";
	} else {
		// let boxHTML = "";
		// for (let i = 0; i < notes_list[index + 1].length; i++) {
		// 	boxHTML += `<span>${notes_list[index + 1][i]}</span>`;
		// }
		// aftertextbox.innerHTML = boxHTML;
		aftertextbox.innerText = notes_list[index + 1]
	}

	index++;

	if (index < notes_list.length) {
		timeoutId = setTimeout(updateTextbox, 60000/speed);
	} else {
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
	speed += 1; 
	tempoTextbox.innerText = speed;
}

function decreaseDelay() {
	// Does not allow delay between notes to go below 1 second
	if (speed > 1) {
		speed -= 1;
	}
	// else{
	//     speedUpBtn.disabled = true;
	// }
	tempoTextbox.innerText = speed;
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
	// resetBtn.style.display = "none"; 
	pauseBtn.style.display = "block"; 
	slowDownBtn.disabled= true;
	speedUpBtn.disabled = true; 
	backBtn.disabled = true;
	forwardBtn.disabled = true;
	index -= 1;
	updateTextbox(); 
}

function resetPage() {
	location.reload();
}

function rewind() {
	// Rewinding is enabled as long as song is not at begenning.
	if (isPaused && index > 1) {
		aftertextbox.innerText = notes_list[index - 1]
		textbox.innerText = notes_list[index - 2];
		index -= 1;
	}
	if (textbox.innerText.length > 4) {
		textbox.style.fontSize = (13 - textbox.innerText.length / 2) + "em";
	} else {
		textbox.style.fontSize = "13em";
	}
}

function forward() {
	// Can only increase index if index is not already at max index
	if (isPaused && index < notes_list.length) {
		textbox.innerText = notes_list[index];
		if (index === notes_list.length-1){
			aftertextbox.innerText = "END";
		} else {
			aftertextbox.innerText = notes_list[index + 1];
		}
		index += 1;
	}
	if (textbox.innerText.length > 4) {
		textbox.style.fontSize = (13 - textbox.innerText.length / 2) + "em";
	} else {
		textbox.style.fontSize = "11em";
	}
}

function startLoop() {
	// Resets index. Clears textbox. Only displays pause button. 
	index = 0;
	textbox.innerText = "";  
	aftertextbox.innerText = ""; 
	playBtn.style.display = "none";
	slowDownBtn.disabled = true;
	speedUpBtn.disabled = true;
	pauseBtn.style.display = "block";   
	tempoTextbox.innerText = speed;
	clearTimeout(timeoutId);
	isPaused = false;
	updateTextbox();
}