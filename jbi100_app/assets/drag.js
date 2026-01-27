/* assets/drag.js */
document.addEventListener("mousedown", function(e) {
    // Verifica se l'elemento cliccato è l'header del radar (o un suo figlio)
    const header = document.getElementById("radar-header");
    const container = document.getElementById("radar-drawer");

    if (!header || !container) return;

    // Se stiamo cliccando dentro l'header
    if (header.contains(e.target) || e.target === header) {
        e.preventDefault(); // Previene la selezione del testo

        // Calcola la posizione iniziale
        let startX = e.clientX;
        let startY = e.clientY;

        // Ottieni la posizione attuale della finestra
        const rect = container.getBoundingClientRect();
        let initialLeft = rect.left;
        let initialTop = rect.top;

        // Funzione che muove la finestra
        function mouseMoveHandler(e) {
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;

            container.style.top = `${initialTop + dy}px`;
            container.style.left = `${initialLeft + dx}px`;

            // Rimuovi 'right' e 'bottom' se presenti per evitare conflitti CSS
            container.style.right = 'auto';
            container.style.bottom = 'auto';
            // Rimuovi trasformazioni che potrebbero interferire
            container.style.transform = 'none';
        }

        // Funzione che ferma il trascinamento
        function mouseUpHandler() {
            document.removeEventListener("mousemove", mouseMoveHandler);
            document.removeEventListener("mouseup", mouseUpHandler);
        }

        // Aggiungi i listener al documento
        document.addEventListener("mousemove", mouseMoveHandler);
        document.addEventListener("mouseup", mouseUpHandler);
    }
});