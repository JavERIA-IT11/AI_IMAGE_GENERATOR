let button = document.getElementById("generatebutton");

button.onclick = function () {

    let input = document.getElementById("prompt").value;

    if (input.trim() === "") {

        alert("Please enter a prompt!");

        return;
    }


    let imagearea = document.getElementById("imagearea");

    let downloadbutton =
        document.getElementById("downloadbutton");


    imagearea.innerHTML = "Generating image...";

    downloadbutton.style.display = "none";


    fetch("/generate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            prompt: input
        })

    })


    .then(response => response.json())


    .then(data => {

        imagearea.innerHTML = "";


        if (data.image) {

            let img = document.createElement("img");

            let imageURL =
                "data:image/png;base64," + data.image;


            img.src = imageURL;

            imagearea.appendChild(img);


            downloadbutton.href = imageURL;

            downloadbutton.style.display = "inline-block";

        }

        else {

            imagearea.textContent =
                "Error: " + data.error;

        }

    })


    .catch(error => {

        imagearea.textContent =
            "Something went wrong: " + error;

    });

};
