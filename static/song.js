let notes = ["A", "B", "C", "D", "E", "F", "G"];
let speed = 5;
let noteIndex = 0;
let elems = {};
let nextNoteTimeout = null;

window.addEventListener("load", () => {
    elems = {
        plusButton: document.getElementById("plus-button"),
        minusButton: document.getElementById("minus-button"),
        currentSpeed: document.getElementById("current-speed"),
        leftNote: document.getElementById("left-note"),
        currentNote: document.getElementById("current-note"),
        rightNote: document.getElementById("right-note"),
        homeButton: document.getElementById("home-button"),
        listButton: document.getElementById("list-button"),
        lastNoteButton: document.getElementById("last-note"),
        playButton: document.getElementById("play"),
        nextNoteButton: document.getElementById("next-note")
    };

    elems.leftNote.innerText = "";
    elems.currentNote.innerText = notes[noteIndex];
    elems.rightNote.innerText = notes[noteIndex + 1];

    elems.currentSpeed.innerText = speed;

    elems.plusButton.addEventListener("click", () => {
        speed = Math.min(10, speed + 1);
        elems.currentSpeed.innerText = speed;
    });

    elems.minusButton.addEventListener("click", () => {
        speed = Math.max(1, speed - 1);
        elems.currentSpeed.innerText = speed;
    });

    elems.playButton.addEventListener("click", () => {
        if (!nextNoteTimeout) {
            nextNoteTimeout = window.setTimeout(showNextNote, 10000 / speed);
        }
    });
});

function showNextNote() {
    noteIndex++;

    elems.leftNote.innerText = elems.currentNote.innerText;
    elems.currentNote.innerText = elems.rightNote.innerText;

    if (noteIndex >= notes.length - 1) {
        elems.rightNote.innerText = "";
    } else {
        elems.rightNote.innerText = notes[noteIndex + 1];
    }

    nextNoteTimeout = window.setTimeout(showNextNote, 10000 / speed);
}