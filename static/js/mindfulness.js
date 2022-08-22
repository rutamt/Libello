export default class Mindfulness {
    constructor(root) {
        // root.innerHTML = Mindfulness.getHTML() // Essentially creates the stuff inside the 'root' or the selected thing its gonna be put inside

        const newMindfulness = document.createElement("div")
        newMindfulness.className = "mindfulness__container col-lg-4 col-md-6 col-sm-12"
        newMindfulness.innerHTML = Mindfulness.getHTML()

        root.appendChild(newMindfulness)

        this.el = { // Selecting important parts of the html code; makes it easier to edit them
            container: root.querySelector(".mindfulness__container"),
            start: root.querySelector(".frame__start"),
            circle: root.querySelector(".frame__circle"),
            breatheIn: root.querySelector(".frame__breathe-in"),
            breatheOut: root.querySelector(".frame__breathe-out"),
            close: root.querySelector(".close__mindfulness"),
        }

        this.BREATHINGINTERVAL = 5000; // Length of each interval of breathing in or out

        this.el.close.addEventListener("click", () => {
            this.el.container.style.display = "none"
        })

        this.el.start.addEventListener("click", () => { // When Clicked . . .
            this.el.start.classList.remove(`frame--active`) // Remove 'frame--active' class to the start button
            // *NOTE frame--active just makes the thing visible and applies a few animations
            this.sequence()

            setTimeout(() => { // Wait until everything is over to then add it back and make it visible
                this.el.start.classList.add(`frame--active`)
            }, this.BREATHINGINTERVAL * 2) // 2 Breaths mean 2 intervals
        })
    }

    breatheIn() { // Breathing in . . .
        this.el.circle.classList.add(`frame__circle--breatheIn`) // Add animation frame for the circle - makes it get larger!
        this.el.breatheIn.classList.add(`frame--active`)

        setTimeout(() => {
            this.el.circle.classList.remove(`frame__circle--breatheIn`) // Removes these two frames and makes them invisible again after interval
            this.el.breatheIn.classList.remove(`frame--active`)
        }, this.BREATHINGINTERVAL)
    }

    breatheOut() {
        this.el.circle.classList.add(`frame__circle--breatheOut`) // Add animation frame for the circle - makes it get smaller!
        this.el.breatheOut.classList.add(`frame--active`)

        setTimeout(() => {
            this.el.circle.classList.remove(`frame__circle--breatheOut`)
            this.el.breatheOut.classList.remove(`frame--active`)
        }, this.BREATHINGINTERVAL)
    }

    sequence() { // Ties all these functions together
        this.breatheIn()

        setTimeout(() => {
            this.breatheOut()
        }, this.BREATHINGINTERVAL)
    }

    static getHTML() { // I could've used javascript to construct the entire thing
        // but to be honest it's actually a lot more efficent to just write out the entire thing and edit parts of that
        return `
            <span class="material-symbols-outlined close__mindfulness">
                close
            </span>

            <button type="button" class="mindfulness__frame frame__start frame--active" type="button">
                <h2>start mindfulness exercise.</h2>
            </button>
            <div class="frame__container">
                <div class="mindfulness__frame frame__circle"></div>
            </div>
            
            <span class="mindfulness__frame frame__breathe-in">
                <h2>Breathe In</h2>
                <span class="material-symbols-outlined">zoom_out_map</span>
                </span>
            <span class="mindfulness__frame frame__breathe-out">
                <h2>Breathe Out</h2>
                <span class="material-symbols-outlined">zoom_in_map</span>
                </span>
        `;
    }


}