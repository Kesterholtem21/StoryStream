var UserComments;
(function (UserComments) {
    UserComments.currentComment = null;
})(UserComments || (UserComments = {}));
document.addEventListener("DOMContentLoaded", () => {
    const adminButtons = document.querySelectorAll(".admin-button");
    adminButtons.forEach(button => {
        button.addEventListener("click", async (event) => {
            const target = event.target;
            const id = target.dataset.id;
            const type = target.dataset.type;
            const isAdmin = target.dataset.isAdmin;
            const parentDiv = button.parentElement;
            const paragraph = parentDiv.querySelector("p");
            if (Number(isAdmin) === 1) {
                button.textContent = button.textContent === "Remove Admin" ? "Add as Admin" : "Remove Admin";
                paragraph.textContent = paragraph.textContent ===
                    "Currently an Admin" ? "Currently a Regular User" : "Currently an Admin";
            }
            else if (Number(isAdmin) === 0) {
                button.textContent = button.textContent === "Add as Admin" ? "Remove Admin" : "Add as Admin";
                paragraph.textContent = paragraph.textContent ===
                    "Currently a Regular User" ? "Currently an Admin" : "Currently a Regular User";
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
    modal.addEventListener("show.bs.modal", activateAdminModal);
});
async function activateAdminModal(event) {
    console.log("GETS HERE");
    UserComments.currentComment = {
        itemID: "",
        userID: "",
        text: "",
        timestamp: "",
        type: "",
        commentID: ""
    };
    const modalCommentDiv = document.getElementById("comments-for-user");
    modalCommentDiv.innerHTML = '';
    const targetBtn = event.relatedTarget;
    const user = targetBtn.dataset.user;
    const type = targetBtn.dataset.type;
    const response = await fetch(`/get_${type}_comments/${user}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    });
    const index = await validateJSON2(response);
    for (const comment of index.commentList) {
        const commentDiv = document.createElement("div");
        modalCommentDiv.appendChild(commentDiv);
        const userLabel = document.createElement("h5");
        const commentField = document.createElement("p");
        const deleteBtn = document.createElement("button");
        deleteBtn.addEventListener("click", async () => {
            removeComment(comment.commentID, comment.type);
            commentDiv.remove();
        });
        const divider = document.createElement("hr");
        deleteBtn.setAttribute("class", "delete-button");
        userLabel.setAttribute("class", "user-paragraph");
        commentDiv.appendChild(divider);
        commentDiv.appendChild(userLabel);
        commentDiv.appendChild(commentField);
        commentDiv.appendChild(deleteBtn);
        deleteBtn.innerText = "DELETE COMMENT";
        commentDiv.appendChild(divider);
        userLabel.innerText = "User " + comment.userID;
        commentField.innerText = comment.text;
    }
}
async function removeComment(commentID, type) {
    console.log(`WOULD DELETE COMMENT: ${commentID} of type ${type}`);
    const response = await fetch(`/deleteComment/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ commentID, type, })
    });
}
function validateJSON2(response) {
    if (response.ok) {
        console.log("IT should BE good");
        return response.json();
    }
    else {
        return Promise.reject(response);
    }
}
