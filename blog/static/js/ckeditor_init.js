(function() {
    function setupMaximize(editorContainer) {
        const toolbar = editorContainer.querySelector('.ck-toolbar__items');
        if (!toolbar || toolbar.querySelector('.ck-maximize-button')) return;

        // Create the button
        const maxBtn = document.createElement('button');
        maxBtn.type = 'button';
        maxBtn.className = 'ck-maximize-button ck ck-button';
        maxBtn.innerHTML = `
            <svg class="ck ck-icon" viewBox="0 0 20 20" width="16" height="16">
                <path d="M2 2h7v2H4v5H2V2zm16 0h-7v2h5v5h2V2zM2 18h7v-2H4v-5H2v7zm16 0h-7v-2h5v-5h2v7z"/>
            </svg>`;
        maxBtn.title = "Toggle Full Screen";

        maxBtn.onclick = function() {
            const isMaximized = editorContainer.classList.toggle('ck-editor-maximized');
            document.body.classList.toggle('ck-no-scroll');
            
            // Optional: Change icon on toggle
            this.style.backgroundColor = isMaximized ? '#eee' : 'transparent';
        };

        toolbar.appendChild(maxBtn);
    }

    // Watch for the editor being added to the DOM
    const observer = new MutationObserver(() => {
        const editors = document.querySelectorAll('.ck-editor');
        editors.forEach(setupMaximize);
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();
