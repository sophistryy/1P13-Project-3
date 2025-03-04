window.addEventListener("load", async () => {
    const response = await fetch("/get_json");
    const data = await response.json();
    const listElem = document.createElement("ul");
    document.body.appendChild(listElem);

    for (const note of data.notes) {
        const noteElem = document.createElement("li");
        listElem.appendChild(noteElem);
        noteElem.innerText = note;
    }
});
