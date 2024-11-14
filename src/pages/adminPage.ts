document.addEventListener("DOMContentLoaded", () => {
    const adminButtons = document.querySelectorAll(".admin-button");
    

    adminButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const target = event.target as HTMLElement;
            const id = target.dataset.id;
            const type = target.dataset.type;

            console.log(id);
            console.log(type);

            if (id && type) {
                try {
                    const response = await fetch("/change_admin/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ id, type }),
                    });
                    if (response.ok) {
                        
                    }
                    else {
                        console.error("Failed to change admin");
                    }
                }
                catch (error) {
                    console.error("Error:", error);
                }
            }
            
        });
    });
});
