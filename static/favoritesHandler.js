document.addEventListener("DOMContentLoaded", () => {
    const favoriteIcons = document.querySelectorAll(".favorite-icon");
    favoriteIcons.forEach((icon) => {
        icon.addEventListener("click", async (event) => {
            const target = event.target;
            const id = target.dataset.id;
            const type = target.dataset.type;
            const isFavorite = target.classList.contains("favorited");
            if (id && type) {
                try {
                    const response = await fetch(isFavorite ? "/remove_favorite" : "/add_favorite", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ id, type }),
                    });
                    if (response.ok) {
                        target.classList.toggle("favorited");
                    }
                    else {
                        console.error("Failed to add favorite");
                    }
                }
                catch (error) {
                    console.error("Error:", error);
                }
            }
        });
    });
});
