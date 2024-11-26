document.addEventListener("DOMContentLoaded", async () => {
    const modal = document.getElementById("formModal");
    modal.addEventListener("show.bs.modal", activateModal);
});
function activateModal(event) {
    console.log("GETS HERE");
    const targetBtn = event.relatedTarget;
    const targetDiv = targetBtn.parentElement;
    const title = targetBtn.dataset.title;
    const author = targetBtn.dataset.author;
    const image = targetBtn.dataset.image;
    const modalImg = document.getElementById("modal-image");
    modalImg.setAttribute("src", image);
    modalImg.setAttribute("alt", "WOMP WOMP");
    const modalTitle = document.getElementById("modal-title");
    modalTitle.innerText = title;
    const modalCreator = document.getElementById("modal-creator");
    modalCreator.innerText = author;
}
