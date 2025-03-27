const upload = async() => {
	let input = document.querySelector('#image-input');

	let data = new FormData()
	data.append('image', input.files[0])

	try {
		const response = await fetch('/get_json', {
			method: "POST",
			body: data
		});

		location.reload();
	} catch  (error) {
		console.error('Error:', error)
	}
};

async function changeName(id, newName, textElem) {
	textElem.innerText = newName;

	const data = new FormData();
	data.append("name", newName);

	await fetch(`/set_name/${id}`, {
		method: "POST",
		body: newName
	});
}

window.addEventListener("load", () => {
	document.querySelector("#image-input").addEventListener('change',upload)

	const colorButton = document.getElementById("color-button");
	
	// colorButton.addEventListener("click", () => {
	// 	const currentTheme = localStorage.getItem("theme");

	// 	if (currentTheme === "blue") {
	// 		localStorage.setItem("theme", "normal");
	// 	} else {
	// 		localStorage.setItem("theme", "blue");
	// 	}    
	// });

	[...document.getElementsByClassName("edit-button")].forEach(elem => {
		elem.addEventListener("click", event => {
			event.stopPropagation();
			const container = elem.parentElement.parentElement.children[0];

			if (container.children[0].style.display === "none") {
				container.children[0].style.display = "initial";
				container.children[1].style.display = "none";
				changeName(container.children[1].dataset["id"], container.children[1].value, container.children[0]);
			} else {
				container.children[0].style.display = "none";
				container.children[1].style.display = "initial";
				container.children[1].value = container.children[0].innerText;
				container.children[1].focus();
			}
		});
	});

	[...document.getElementsByClassName("change-name-input")].forEach(elem => {
		const container = elem.parentElement;

		elem.addEventListener("blur", event => {
			if (event.relatedTarget && event.relatedTarget.className.includes("edit-button")) {
				return;
			}
			container.children[0].style.display = "initial";
			container.children[1].style.display = "none";
			changeName(container.children[1].dataset["id"], container.children[1].value, container.children[0]);
		});

		elem.addEventListener("keydown", event => {
			if (event.key.toLowerCase() === "escape") {
				container.children[0].style.display = "initial";
				container.children[1].style.display = "none";
			} else if (event.key.toLowerCase() === "enter") {
				container.children[0].style.display = "initial";
				container.children[1].style.display = "none";
				changeName(container.children[1].dataset["id"], container.children[1].value, container.children[0]);
			}
		});
	});
});
