function shuffleText(element, finalLetter) {
    let letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let index = 0;
    let interval = setInterval(() => {
        element.textContent = letters[Math.floor(Math.random() * letters.length)];
        index++;
        if (index > 10) { 
            clearInterval(interval);
            element.textContent = finalLetter;
        }
    }, 100);
}

document.addEventListener("DOMContentLoaded", () => {
    let finalText = ["S", "C", "H", "E", "M", "A", "S", "P", "H", "E", "R", "E", ];
    let spans = document.querySelectorAll(".shuffle");

    spans.forEach((span, index) => {
        setTimeout(() => {
            shuffleText(span, finalText[index]);
        }, index * 200);
    });
});
