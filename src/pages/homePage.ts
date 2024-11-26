document.addEventListener("DOMContentLoaded", async () => {
    

    const modal = document.getElementById("formModal");
    modal.addEventListener("show.bs.modal",activateModal);

});


function activateModal(event: MouseEvent){
    console.log("GETS HERE")

    const targetBtn = event.relatedTarget as HTMLElement;
    const targetDiv = targetBtn.parentElement;
    const title = targetBtn.dataset.title;
    const author = targetBtn.dataset.author;
    const image = targetBtn.dataset.image;

    const modalImg = document.getElementById("modal-image");
    modalImg.setAttribute("src", image);
    modalImg.setAttribute("alt","WOMP WOMP");

    const modelTitle = document.getElementById("model-title");
    modalImg.innerText = title;
    
    const modelCreator = document.getElementById("model-creator");
    modelCreator.innerText = author;

}