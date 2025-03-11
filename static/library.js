const song_list = [
    "Song #1",
    "Song #2",
    "Song #3",
    "Song #4",
];

function libary_list(songs) {
    // Get the container element where the buttons will be added
    const container = document.getElementById("buttonsContainer");

    // Loop through the songs array and create a button for each song
    for (let i = 0; i < songs.length; i++) {
        const song = songs[i];

        // Create a new button
        const newButton = document.createElement("button");

        // Set the button's text
        newButton.textContent = `Play: ${song}`;

        // Add an event listener to each button (you can customize the behavior)
        newButton.onclick = function () {
            alert(`Now playing: ${song}`);
        };

        // Append the new button to the container
        container.appendChild(newButton);
    }
}

libary_list(song_list)
