document.addEventListener("DOMContentLoaded", () => {
    const adminButtons = document.querySelectorAll<HTMLButtonElement>(".admin-button");
    

    adminButtons.forEach(button => {

        

        button.addEventListener("click", async (event) => {
            const target = event.target as HTMLButtonElement;
            const id = target.dataset.id;
            const type = target.dataset.type;
            const isAdmin = target.dataset.isAdmin;
            const parentDiv = button.parentElement;
            const paragraph = parentDiv.querySelector("p");
            
            if(Number(isAdmin) === 1){
                button.textContent = button.textContent === "Remove Admin" ? "Add as Admin" : "Remove Admin";
                paragraph.textContent = paragraph.textContent === 
                "Currently an Admin" ? "Currently a Regular User" : "Currently an Admin"
            }
            else if(Number(isAdmin) ===  0){
                button.textContent = button.textContent === "Add as Admin" ? "Remove Admin" : "Add as Admin";
                paragraph.textContent = paragraph.textContent === 
                "Currently a Regular User" ? "Currently an Admin" : "Currently a Regular User"
            }

            
            
            

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


    const modal = document.getElementById("commentModal");
    modal.addEventListener("show.bs.modal",activateModal);

    async function activateModal(event: MouseEvent){
        console.log("GETS HERE");
        Comments.currentComment = {
            itemID: "",
            userID: "",
            text: "",
            timestamp: "",
            type: "",
        };
    
        //moving on to comments
        const modalCommentDiv = document.getElementById("comments-for-user");
        const targetBtn = event.relatedTarget as HTMLElement;
        const user = targetBtn.dataset.user;
        const type = targetBtn.dataset.type;
    
        
    
    
        const response = await fetch(`/get_${type}_comments?userID=${user}`, {
            method:  "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        const index = <Comments.CommentList> await validateJSON(response);
        
        for (const comment of index.commentList) {
            const userLabel = document.createElement("h5");
            const commentField = document.createElement("p");

            modalCommentDiv.appendChild(userLabel);
            modalCommentDiv.appendChild(commentField);

            userLabel.innerText = "User " + comment.userID;
            commentField.innerText = comment.text;
        }
    }

});
