export default class Timer {
    constructor(root) {
        root.innerHTML = Timer.getHTML();

        // References each of the parts of the timer

        this.el = {
            minutes: root.querySelector(".timer__part--minutes"),
            seconds: root.querySelector(".timer__part--seconds"),
            control: root.querySelector(".timer__btn--control"),
            reset: root.querySelector(".timer__btn--reset"),
        };

        this.interval = null; // Use the setinterval function in java to make the timer trigger.
        // Its null because the timer has to start up not running.
        this.remainingSeconds = 0; // Current remaining seconds

        // EventListeners for the buttons ie. check if they are clicked
        this.el.control.addEventListener("click", () => {
            if (this.interval === null) { // Is there an interval going?
                this.start();
            } else {
                this.stop();
            }

        });

        this.el.reset.addEventListener("click", () => { // Prompt user for time input
            const inputMinutes = prompt("Enter number of minutes:"); // Opens up a prompt in the browser

            if (inputMinutes < 60) {
                this.stop(); // Stop before you set a new time
                this.remainingSeconds = inputMinutes * 60;
                this.updateInterfaceTime();
            }
        });

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
            this.el.control.innerHTML = `<i class="fa-solid fa-play"></i>`; // Set icon to play
            this.el.control.classList.add("timer__btn--start"); // Adds start class
            this.el.control.classList.remove("timer__btn--stop"); // Removes stop class
        } else { // So if the timer IS running . . .
            this.el.control.innerHTML = `<i class="fa-solid fa-pause"></i>`; // Set icon to stop
            this.el.control.classList.add("timer__btn--stop"); // Adds stop class
            this.el.control.classList.remove("timer__btn--start"); // Removes start class
        }
    }

    // Start/Stop

    start() { // Basically we gotta do some stuff to get it to work
        if (this.remainingSeconds === 0) return; // If there are already remaining seconds we can just return and cancel out current operation
        // If not we do smth interesting
        this.interval = setInterval(() => { // This code runs every second
            this.remainingSeconds-- ; // Remove a second every second
            this.updateInterfaceTime(); // Update timer

            if (this.reaminingSeconds === 0) {
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

    // User Interface

    static getHTML() {
        return `
            <span class="timer__part timer__part--minutes">00</span>
            <span class="timer__part">:</span>
            <span class="timer__part timer__part--seconds">00</span>
            <button type="button" class="timer__btn timer__btn--control timer__btn--start">
                <i class="fa-solid fa-play"></i>
            </button>
            <button type="button" class="timer__btn timer__btn--control timer__btn--reset">
                <i class="fa-solid fa-clock"></i>
            </button>
        `;
    }


}



// Logic