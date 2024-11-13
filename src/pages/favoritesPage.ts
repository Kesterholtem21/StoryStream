class ViewContainer extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        
        // Clone and attach content
        const template = document.createElement('template');
        template.innerHTML = `
            <slot></slot>
        `;
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }
}

// Define the custom element
customElements.define('view-container', ViewContainer);

// Toggle logic for switching between grid and list view
const toggleButton = document.getElementById("toggleView");
const viewContainer = document.querySelector("view-container");

toggleButton.addEventListener("click", () => {
    viewContainer.classList.toggle("grid-view");
    viewContainer.classList.toggle("list-view");
});
