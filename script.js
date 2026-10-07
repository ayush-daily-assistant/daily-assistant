// =========================
// REMINDER NOTIFICATIONS
// =========================

let notifiedReminders = [];


function requestNotificationPermission() {

    if ("Notification" in window) {

        if (Notification.permission === "default") {

            Notification.requestPermission();

        }

    }

}


function checkReminders() {

    fetch("/api/reminders")
        .then(response => response.json())
        .then(reminders => {

            const currentTime = new Date();

            reminders.forEach(reminder => {

                if (reminder.completed === 1) {
                    return;
                }

                const reminderTime = new Date(reminder.time);

                const reminderKey = reminder.id;

                if (
                    reminderTime <= currentTime &&
                    !notifiedReminders.includes(reminderKey)
                ) {

                    if (
                        "Notification" in window &&
                        Notification.permission === "granted"
                    ) {

                        new Notification(
                            "⏰ Personal Daily Assistant",
                            {
                                body: reminder.title
                            }
                        );

                    }

                    notifiedReminders.push(reminderKey);

                }

            });

        })

        .catch(error => {
            console.log("Reminder error:", error);
        });

}


requestNotificationPermission();

checkReminders();

setInterval(checkReminders, 30000);

// =========================
// THEME SYSTEM
// =========================

const themeSelector = document.getElementById("themeSelector");


// Load saved theme

const savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {

    document.body.classList.add("dark-theme");

}


// Set selector to saved theme

if (themeSelector && savedTheme) {

    themeSelector.value = savedTheme;

}


// Change theme

if (themeSelector) {

    themeSelector.addEventListener("change", function () {

        if (this.value === "dark") {

            document.body.classList.add("dark-theme");

            localStorage.setItem("theme", "dark");

        } else {

            document.body.classList.remove("dark-theme");

            localStorage.setItem("theme", "light");

        }

    });

}