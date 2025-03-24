const upload = async() => {
    let input = document.querySelector('#image-input');

    let data = new FormData()
    data.append('image', input.files[0])

    try {
        const response = await fetch('/get_json', {
            method: "POST",
            body: data
        });

        const responseText = await response.text();
        console.log('Response', responseText);
    } catch  (error) {
        console.error('Error:', error)
    }
};

document.querySelector("#image-input").addEventListener('change',upload)

