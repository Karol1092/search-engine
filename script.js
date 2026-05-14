const API = "http://127.0.0.1:8000";

async function searchResults() {
    const inputText = document.getElementById("input").value;
    const backendType = document.getElementById("backend").value;

    const res = await fetch(`${API}/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText, backend: backendType })
    });

    const data = await res.json();

    const list = document.getElementById("results");
    list.innerHTML = "";

    data.results.forEach(result => {
        const li = document.createElement("li");

        let scoreClass = "";

        if (result.score >= 70) scoreClass = "good";
        else if (result.score >= 30) scoreClass = "medium";
        else scoreClass = "bad";

        li.innerHTML = `
            <div class="results">
                <p class="title">${result.title}</p>
                <a class="link" href="${result.url}" target="_blank">${result.url}</a>
                <p class="score ${scoreClass}" >${result.score}%</p>
            </div>
        `;

        list.append(li);
    });
}