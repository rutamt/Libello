// Issues; code is asynchronous bc the timeout functions and the classremove/add is not working

export default class Mindfulness {
    constructor(root) {
        root.innerHTML = Mindfulness.getHTML()

        this.el = {
            start: root.querySelector(".mindfulness--start"),
            circle: root.querySelector(".mindfulness__breathing-circle"),
            breatheIn: root.querySelector(".mindfulness__frame--breathe-in"),
            breatheOut: root.querySelector(".mindfulness__frame--breathe-out"),
        }

        this.el.start.addEventListener("click", () => {
            console.log("Got Clicked")
            this.el.start.classList.remove(`mindfulness--visible`)
            this.sequence()
        })
    }

    breatheIn() {
        this.el.circle.classList.add(`anim--breathe__in`)
        this.el.breatheIn.classList.add(`mindfulness--visible`)
        console.log("Breathing In")
        // setTimeout(() => {
        //     this.el.circle.classList.remove(`anim--breathe__in`)
        // }, 7000)
    }
    breatheOut() {
        this.el.circle.classList.add(`anim--breathe__out`)
        this.el.breatheOut.classList.add(`mindfulness--visible`)
        console.log("Breathing Out")
        // setTimeout(() => {
        //     this.el.circle.classList.remove(`anim--breathe__out`)
        // }, 7000)
    }

    sequence() {
        console.log("I am sequencing . . .")
        this.el.circle.classList.add(`mindfulness--visible`)
        this.el.start.classList.remove(`mindfulness--visible`)
        this.breatheIn()
        setTimeout(() => {
            this.el.circle.classList.remove(`anim--breathe__in`)
            this.el.breatheIn.classList.remove(`mindfulness--visible`)
            this.breatheOut()
            console.log("Finished breathein")

            setTimeout(() => {
                this.el.breatheOut.classList.remove(`mindfulness--visible`)
                this.el.start.classList.add(`mindfulness--visible`)
                this.el.circle.classList.remove(`anim--breathe__out`)
                console.log("Finished breatheout")
                this.el.start.classList.add(`mindfulness--visible`)
                this.el.circle.classList.remove(`mindfulness--visible`)
            }, 7000)
        }, 7000)
    }

    static getHTML() {
        return `
        <div class="mindfulness__container">
            <span class="mindfulness mindfulness__frame mindfulness__frame--breathe-in">
                <p>Breathe In</p>
                <i class="fa-solid fa-down-left-and-up-right-to-center"></i>
                </span>
            <span class="mindfulness mindfulness__frame mindfulness__frame--breathe-out">
                <p>Breathe Out</p>
                <i class="fa-solid fa-up-right-and-down-left-from-center"></i>
                </span>
            <div class="mindfulness mindfulness__breathing-circle">
            </div>
            <button type="button" class="mindfulness mindfulness--start shrink-border mindfulness--visible" type="button">
                Start Mindfulness Exercise
            </button>
        </div>
        `;
    }


}