document.addEventListener("DOMContentLoaded", () => {
    const tabButtons = document.querySelectorAll(".tab-button");
    const tabContents = document.querySelectorAll(".tab-content");

    tabButtons.forEach(button => {
        button.addEventListener("click", (event) => {
            tabButtons.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(content => content.classList.remove("active"));

            const tabName = (event.target as HTMLElement).getAttribute("data-tab");
            if (tabName) {
                (document.getElementById(tabName) as HTMLElement).classList.add("active");
                (event.target as HTMLElement).classList.add("active");
            }
        });
    });
});
