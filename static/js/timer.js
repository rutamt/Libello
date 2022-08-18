// https://www.youtube.com/watch?v=PIiMSMz7KzM
export default class Timer {
    constructor(root) {

        const newTimer = document.createElement("div")
        newTimer.className = "timer__container timer__container--timer col-lg-4 col-md-6 col-sm-12"
        newTimer.innerHTML = Timer.getHTML()

        root.appendChild(newTimer)


        // References each of the parts of the timer

        this.el = {
            container: root.querySelector(".timer__container"),
            minutes: root.querySelector(".timer__part--minutes"),
            seconds: root.querySelector(".timer__part--seconds"),
            startStop: root.querySelector(".timer__btn--start-stop"),
            reset: root.querySelector(".timer__btn--control"),
            pomodoro: root.querySelector(".timer__btn--pomo"),
        };

        this.interval = null; // Use the setinterval function in java to make the timer trigger.
        // Its null because the timer has to start up not running.
        this.remainingSeconds = 0; // Current remaining seconds

        this.ispomodoro = false;

        // EventListeners for the buttons ie. check if they are clicked
        this.el.startStop.addEventListener("click", () => {
            if (this.interval === null) { // Is there an interval going?
                this.start();
            } else {
                this.stop();
            }

        });

        this.el.reset.addEventListener("click", () => { // Prompt user for time input
            if (this.ispomodoro) {
                this.stop();
                if (this.pomo) {
                    this.remainingSeconds = 1500;
                    this.el.reset.classList.replace("timer__btn--work", "timer__btn--break")
                    this.el.reset.innerHTML = "Break"
                } else {
                    this.remainingSeconds = 300;
                    this.el.reset.classList.replace("timer__btn--break", "timer__btn--work")
                    this.el.reset.innerHTML = "Work"
                }
                this.updateInterfaceTime();
                this.pomo = !this.pomo;
            } else {
                const inputMinutes = prompt("Enter number of minutes:"); // Opens up a prompt in the browser

                if (inputMinutes < 60) {
                    if (inputMinutes > 0) {
                        this.stop(); // Stop before you set a new time
                        this.remainingSeconds = inputMinutes * 60;
                        this.updateInterfaceTime();
                    }
                }
            }
        });

        this.el.pomodoro.addEventListener("click", () => {
            this.pomo = true;
            this.pomofy()
        })

    }

    // Interface time updater

    updateInterfaceTime() {
        // Calculate minutes from seconds
        const minutes = Math.floor(this.remainingSeconds / 60); // Minutes are 60 seconds
        const seconds = this.remainingSeconds % 60; // Remainder of the minutes division

        this.el.minutes.textContent = minutes.toString().padStart(2, "0"); // Basically the pad start padds it if it is less than 2 and the 0 means to fill the extra space with 0 if the number only takes 1 space.
        this.el.seconds.textContent = seconds.toString().padStart(2, "0");
    }

    // Update the Buttons

    updateInterfaceControls() { //Check whether the timer is running
        if (this.interval === null) { // If timer(interval) is not running . . .
            this.el.startStop.innerHTML = `<span class="material-symbols-outlined">play_arrow</span>`; // Set icon to play
            this.el.startStop.classList.replace("timer__btn--stop", "timer__btn--start"); // Adds start class
        } else { // So if the timer IS running . . .
            this.el.startStop.innerHTML = `<span class="material-symbols-outlined">pause</span>`; // Set icon to stop
            this.el.startStop.classList.replace("timer__btn--start", "timer__btn--stop"); // Adds stop class
        }
    }

    // Start/Stop

    start() { // Basically we gotta do some stuff to get it to work
        if (this.remainingSeconds === 0) return; // If there are already remaining seconds we can just return and cancel out current operation
        // If not we do smth interesting
        this.interval = setInterval(() => { // This code runs every second
            this.remainingSeconds--; // Remove a second every second
            this.updateInterfaceTime(); // Update timer

            if (this.remainingSeconds === 0) {
                this.stop(); // Another function
            }

        }, 1000) // The setInterval function allows for code to run on a timer. The 1000 is 1000 miliseconds or one second

        this.updateInterfaceControls();
    }

    stop() {
        clearInterval(this.interval); // Stops the function above

        this.interval = null; // Clears the interval

        this.updateInterfaceControls(); // Displays the updated buttons
    }

    pomofy() {
        this.stop()
        this.remainingSeconds = 0;

        this.el.pomodoro.classList.toggle("timer__btn--timer")
        this.el.pomodoro.classList.toggle("timer__btn--pomodoro")

        this.el.container.classList.toggle("timer__container--timer")
        this.el.container.classList.toggle("timer__container--pomo")

        if (!this.ispomodoro) {
            this.el.pomodoro.innerHTML = "TIMER"

            this.el.reset.classList.replace("timer__btn--reset", "timer__btn--work")
            this.el.reset.innerHTML = "Work"

            this.ispomodoro = true
        } else {
            this.el.pomodoro.innerHTML = "POMODORO"

            this.el.reset.classList.remove("timer__btn--work", "timer__btn__break")
            this.el.reset.classList.add("timer__btn--reset")
            this.el.reset.innerHTML = '<span class="material-symbols-outlined">timer</span>'
            this.ispomodoro = false
        }

        this.updateInterfaceTime()
    }

    // User Interface

    static getHTML() {
        return `
            <div class="timer">
                <span class="timer__part timer__part--minutes">00</span>
                <span class="timer__part">:</span>
                <span class="timer__part timer__part--seconds">00</span>
            </div>

            <div class="timer__buttons">

                <!-- Find a way to insert <span class="material-symbols-outlined">pause</span> into a class -->

                <button type="button" class="timer__btn timer__btn--start-stop timer__btn--start">
                    <span class="material-symbols-outlined">play_arrow</span>
                    </button>
                <button type="button" class="timer__btn timer__btn--control timer__btn--reset">
                    <span class="material-symbols-outlined">timer</span>
                    </button>
                <button type="button" class="timer__btn timer__btn--pomo timer__btn--pomodoro">
                    POMODORO
                    </button>
            </div>
        `;
    }


}



// Logic