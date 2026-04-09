function searchCourses() {
    const input = document.getElementById("search").value.toLowerCase();
    const cards = document.getElementsByClassName("course-card");

    for (let i = 0; i < cards.length; i++) {
        const title = cards[i].getElementsByTagName("h2")[0].innerText.toLowerCase();
        cards[i].style.display = title.includes(input) ? "flex" : "none";
    }
}
