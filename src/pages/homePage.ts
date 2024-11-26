namespace Comments{
    export interface CommentList{
        comments : Array<Comment>;
    }

    export interface Comment{
        user_id : number;
        text : string;
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    

    const modal = document.getElementById("formModal");
    modal.addEventListener("show.bs.modal",activateModal);

});


async function activateModal(event: MouseEvent){
    console.log("GETS HERE")

    const targetBtn = event.relatedTarget as HTMLElement;
    const targetDiv = targetBtn.parentElement;
    const title = targetBtn.dataset.title;
    const author = targetBtn.dataset.author;
    const image = targetBtn.dataset.image;
    const user = targetBtn.dataset.user;
    const book = targetBtn.dataset.bookId;
    const type = targetBtn.dataset.book;

    const modalImg = document.getElementById("modal-image");
    modalImg.setAttribute("src", image);
    modalImg.setAttribute("alt","WOMP WOMP");

    const modelTitle = document.getElementById("model-title");
    modalImg.innerText = title;
    
    const modelCreator = document.getElementById("model-creator");
    modelCreator.innerText = author;

    const commentDiv = document.getElementById("comments-for-item")
    const response = await fetch("/get_comments", {
            method:  "GET",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({user,book,type})
    });

    const index = <Comments.CommentList> await validateJSON(response);
    
    for(const comment of index.comments){
        const userLabel = document.createElement("h5");
        const commnetField = document.createElement("p");

        targetDiv.appendChild(userLabel);
        targetDiv.appendChild(commnetField);

        userLabel.innerText = "User " + comment.user_id;
        commnetField.innerText = comment.text;
    }

}

function validateJSON(response: Response) {
    if (response.ok) {
        console.log("IT should BE good")
        return response.json();
    } else {
        return Promise.reject(response);
    }
}