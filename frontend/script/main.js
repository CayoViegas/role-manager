BASE_URL = "http://localhost:5000";

document.querySelector("#login-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const username = document.querySelector("#username");
    const password = document.querySelector("#password");

    try {
        const response = await fetch(BASE_URL + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username.value,
                password: password.value,
            }),
        });

        const data = await response.json();
        const statusCode = response.status;

        if (statusCode === 201 && data.token) {
            localStorage.setItem("token", data.token);
            localStorage.setItem("username", username.value); // Armazenar o nome do usuário
            window.location.href = "characters.html";
        } else {
            console.error("Erro no login");
        }
    } catch (error) {
        console.error("Error:", error);
    }
});