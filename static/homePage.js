document.addEventListener("DOMContentLoaded", async () => {
    const modal = document.getElementById("formModal");
    modal.addEventListener("show.bs.modal", activateModal);
});
async function activateModal(event) {
    console.log("GETS HERE");
    const targetBtn = event.relatedTarget;
    const targetDiv = targetBtn.parentElement;
    const title = targetBtn.dataset.title;
    const author = targetBtn.dataset.author;
    const image = targetBtn.dataset.image;
    const user = targetBtn.dataset.user;
    const item = targetBtn.dataset.itemId;
    const type = targetBtn.dataset.type;
    console.log(user);
    console.log(item);
    console.log(type);
    const modalImg = document.getElementById("modal-image");
    modalImg.setAttribute("src", image);
    modalImg.setAttribute("alt", "WOMP WOMP");
    const modelTitle = document.getElementById("modal-title");
    modalImg.innerText = title;
    const modelCreator = document.getElementById("modal-creator");
    modelCreator.innerText = author;
    const commentDiv = document.getElementById("comments-for-item");
    let index = [];
    if (type === "Book") {
        const response = await fetch("/get_book_comments", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        index = await validateJSON(response);
    }
    if (type === "Movie") {
        const response = await fetch("/get_comments", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        index = await validateJSON(response);
    }
    const commentList = index["comments"];
    console.log(typeof (index));
    console.log(index);
    console.log(commentList);
    for (const comment of commentList) {
        console.log(comment.detailList);
        for (const detail of comment.detailList) {
            if (detail.item_id === Number(item)) {
                console.log(comment);
                const userLabel = document.createElement("h5");
                const commnetField = document.createElement("p");
                targetDiv.appendChild(userLabel);
                targetDiv.appendChild(commnetField);
                userLabel.innerText = "User " + detail.user_id;
                commnetField.innerText = detail.text;
            }
        }
    }
    const addCommentInput = document.getElementById("comment-input");
    addCommentInput.value = "";
    const submitBtn = document.getElementById("sumbit-comment");
    submitBtn.addEventListener("click", function () {
        submitComment(item, user, addCommentInput.innerText, type);
    });
}
async function submitComment(itemId, user_id, text, type) {
    const addCommentInput = document.getElementById("comment-input");
    const response = await fetch("/post_comments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ itemId, user_id, text, type })
    });
    const dbResponse = await validateJSON(response);
    console.log(dbResponse);
}
function validateJSON(response) {
    if (response.ok) {
        console.log("IT should BE good");
        return response.json();
    }
    else {
        return Promise.reject(response);
    }
}
