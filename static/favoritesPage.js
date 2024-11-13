class ViewContainer extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        const template = document.createElement('template');
        template.innerHTML = `
            <slot></slot>
        `;
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }
}
customElements.define('view-container', ViewContainer);
const toggleButton = document.getElementById("toggleView");
const viewContainer = document.querySelector("view-container");
toggleButton.addEventListener("click", () => {
    viewContainer.classList.toggle("grid-view");
    viewContainer.classList.toggle("list-view");
});
