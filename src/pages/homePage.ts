namespace Comments{
    export interface Comment{
        userID : number;
        itemID: number;
        text: string;
        timestamp: string;
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

    

});

async function activateModal(event: MouseEvent){
    console.log("GETS HERE");
    
    const modalCommentDiv = document.getElementById("comments-for-item")
    modalCommentDiv.innerHTML = '';
    const targetBtn = event.relatedTarget as HTMLElement;
    const targetDiv = targetBtn.parentElement;
    const title = targetBtn.dataset.title;
    const author = targetBtn.dataset.author;
    const image = targetBtn.dataset.image;

    const user = targetBtn.dataset.user;
    const item = targetBtn.dataset.itemId;
    const type = targetBtn.dataset.type;


    console.log(type);

    const modalImg = document.getElementById("modal-image");
    modalImg.setAttribute("src", image);
    modalImg.setAttribute("alt","WOMP WOMP");

    const modelTitle = document.getElementById("modal-title");
    modalImg.innerText = title;
    
    const modelCreator = document.getElementById("modal-creator");
    modelCreator.innerText = author;


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
            if(comment.itemID === Number(item)){
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
    
    const submitBtn = document.getElementById("sumbit-comment");

    submitBtn.addEventListener("click", function(){
         submitComment(item,user,addCommentInput.value, type)
    });


}




async function submitComment(itemId: string, user_id: string, text: string, type: string){
    const addCommentInput = document.getElementById("comment-input");
    const response = await fetch("/post_comments", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({itemId,user_id,text,type})
    });

    const dbResponse = await validateJSON(response);
}

function validateJSON(response: Response) {
    if (response.ok) {
        console.log("IT should BE good")
        return response.json();
    } else {
        return Promise.reject(response);
    }
}