// filepath: c:\Users\ikerr\OneDrive\Documentos\CosasGithub\TEPGD\feelingsSwitch2\web-app\src\js\script.js

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("parameterForm");
    const qntPostsInput = document.getElementById("qntPosts");
    const cntMaxInput = document.getElementById("cntMax");
    const startDateInput = document.getElementById("startDate");
    const endDateInput = document.getElementById("endDate");
    const submitButton = form.querySelector("button[type='submit']");
    
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        
        // Deshabilitar el botón de envío
        submitButton.disabled = true;
        submitButton.textContent = "Processing...";

        const qntPosts = qntPostsInput.value;
        const cntMax = cntMaxInput.value;
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        
        const params = {
            qntPosts: qntPosts,
            cntMax: cntMax,
            startDate: startDate,
            endDate: endDate
        };
        
        fetch("/run-script", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
            alert("Script executed successfully!"); // Alert when the process finishes successfully
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred while executing the script."); // Alert in case of an error
        })
        .finally(() => {
            // Habilitar el botón de envío nuevamente
            submitButton.disabled = false;
            submitButton.textContent = "Accept";
        });
    });
});