document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");
    tabButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            tabButtons.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));
            const tabName = event.target.getAttribute("data-tab");
            if (tabName) {
                document.getElementById(tabName).classList.add("active");
                event.target.classList.add("active");
            }
        });
    });
});
