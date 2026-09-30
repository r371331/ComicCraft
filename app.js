document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("comic-form");
    const button = document.getElementById("generate-btn");
    const status = document.getElementById("status");

    if (!form) return;

    form.addEventListener("submit", () => {
        button.disabled = true;
        button.textContent = "Generating…";
        status.textContent = "Creating the story, artwork, and PDF. Please wait.";
    });
});
