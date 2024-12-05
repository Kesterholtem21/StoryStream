namespace Comments{
    export let currentComment: Comment | null = null;

    export interface Comment{
        userID : string;
        itemID: string;
        text: string;
        timestamp: string;
        type: string;
    }

    export interface CommentList{
        success: boolean;
        commentList: Array<Comment>
    }
}


document.addEventListener("DOMContentLoaded", async () => {
    

    const modal = document.getElementById("formModal");
    modal.addEventListener("show.bs.modal",activateModal);

    const submitBtn = document.getElementById("sumbit-comment");
    //submitBtn.replaceWith(submitBtn.cloneNode(true));
    submitBtn.addEventListener("click", async() => {
        console.log("SUBMITTED");
        submitComment(
            Comments.currentComment.itemID,
            Comments.currentComment.userID,
            Comments.currentComment.text,
            Comments.currentComment.type
        );
    }
    

);
});



async function activateModal(event: MouseEvent){
    console.log("GETS HERE");
    Comments.currentComment = {
        itemID: "",
        userID: "",
        text: "",
        timestamp: "",
        type: "",
    };
    
    const modalCommentDiv = document.getElementById("comments-for-item")
    modalCommentDiv.innerHTML = '';
    const targetBtn = event.relatedTarget as HTMLElement;
    const targetDiv = targetBtn.parentElement;
    const title = targetBtn.dataset.title;
    const author = targetBtn.dataset.author;
    const image = targetBtn.dataset.image;
    const genres = targetBtn.dataset.genres;
    const description = targetBtn.dataset.description;
    console.log(genres);

    const user = targetBtn.dataset.user;
    const item = targetBtn.dataset.itemId;
    const type = targetBtn.dataset.type;


    console.log(type);

    const modalImg = document.getElementById("modal-image");
    modalImg.setAttribute("src", image);
    modalImg.setAttribute("alt","WOMP WOMP");

    const modelTitle = document.getElementById("modal-title");
    modelTitle.innerText = title;
    
    const modelCreator = document.getElementById("modal-creator");
    modelCreator.innerText = author;

    const modelGenre = document.getElementById("modal-genre");
    modelGenre.innerText = genres;

    const modalDescription = document.getElementById("modal-description");
    modalDescription.innerText = description;

    //moving on to comments
    const commentDiv = document.getElementById("comments-for-item");

    


    const response = await fetch(`/get_${type}_comments`, {
        method:  "GET",
        headers: {
            "Content-Type": "application/json",
        }
    });
    const index = <Comments.CommentList> await validateJSON(response);
    
    for(const comment of index.commentList){
            if(String(comment.itemID) === item){
                console.log("MAKES IT IN HERE")
                console.log(comment);
                const userLabel = document.createElement("h5");
                const commnetField = document.createElement("p");
    
                modalCommentDiv.appendChild(userLabel);
                modalCommentDiv.appendChild(commnetField);


    
                userLabel.innerText = "User " + comment.userID;
                commnetField.innerText = comment.text;
            }  
    }

    const addCommentInput = <HTMLInputElement> document.getElementById("comment-input");
    addCommentInput.value = "";

    Comments.currentComment.itemID = item;
    Comments.currentComment.userID = user;
    Comments.currentComment.text = addCommentInput.value;
    Comments.currentComment.type = type;
}




async function submitComment(itemId: string, user_id: string, text: string, type: string){
    const addCommentInput = <HTMLInputElement> document.getElementById("comment-input");
    Comments.currentComment.text = addCommentInput.value;
    text = Comments.currentComment.text;
    const response = await fetch("/post_comments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({itemId,user_id,text,type})
    });

    const modalCommentDiv = document.getElementById("comments-for-item");
    const userLabel = document.createElement("h5");
    const commentField = document.createElement("p");
    
    modalCommentDiv.appendChild(userLabel);
    modalCommentDiv.appendChild(commentField);

    userLabel.innerText = `User ${user_id}`;
    commentField.innerText = text;
    addCommentInput.value = "";
    
    
}

function validateJSON(response: Response) {
    if (response.ok) {
        console.log("IT should BE good")
        return response.json();
    } else {
        return Promise.reject(response);
    }
}