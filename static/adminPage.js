document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".admin-button");
    tabButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            const tabName = event.currentTarget.getAttribute("data-tab");
            if (tabName) {
                document.getElementById("movies")?.classList.remove("active");
                document.getElementById("books")?.classList.remove("active");
                tabButtons.forEach(btn => btn.classList.remove("active"));
                document.getElementById(tabName)?.classList.add("active");
                button.classList.add("active");
            }
        });
    });
});
