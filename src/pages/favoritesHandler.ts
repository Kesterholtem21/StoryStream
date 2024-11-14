document.addEventListener("DOMContentLoaded", () => {
    const favoriteIcons = document.querySelectorAll<HTMLElement>(".favorite-icon");

    favoriteIcons.forEach((icon) => {
        icon.addEventListener("click", async (event) => {
            const target = event.target as HTMLElement;
            const id = target.dataset.id;
            const type = target.dataset.type;

            if (id && type) {
                try {
                    const response = await fetch("/add_favorite", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ id, type }),
                    });

                    if (response.ok) {
                        target.classList.toggle("favorited");
                    } else {
                        console.error("Failed to add favorite");
                    }
                } catch (error) {
                    console.error("Error:", error);
                }
            }
        });
    });
});
