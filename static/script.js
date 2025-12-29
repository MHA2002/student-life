document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll("tr[data-due]");

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const inDays = (d) => {
        const x = new Date(today);
        x.setDate(x.getDate() + d);
        return x;
    };

    rows.forEach((row) => {
        const dueStr = row.getAttribute("data-due"); // YYYY-MM-DD
        if (!dueStr) return;

        const due = new Date(dueStr + "T00:00:00");
        if (isNaN(due.getTime())) return;

        if (due < today) {
            row.classList.add("due-overdue");
            return;
        }

        if (due <= inDays(3)) {
            row.classList.add("due-soon");
        }
    });
});
