const BASE_URL = "http://localhost:5000";

// Função para processar o formulário de cadastro
document.querySelector("#signup-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
    const isSuperuser = document.querySelector("#is_superuser").checked;

    try {
        const response = await fetch(`${BASE_URL}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
                is_superuser: isSuperuser,
            }),
        });
        
        const data = await response.json();

        if (response.status === 201) {
            // Cadastro bem-sucedido
            document.querySelector("#signup-message").textContent = "Cadastro realizado com sucesso!";
            document.querySelector("#signup-message").style.color = "green";

            // Redirecionar para a página de login após alguns segundos
            setTimeout(() => {
                window.location.href = "index.html";
            }, 2000);
        } else {
            // Erro no cadastro
            document.querySelector("#signup-message").textContent = data.message || "Erro ao realizar cadastro";
            document.querySelector("#signup-message").style.color = "red";
        }
    } catch (error) {
        console.error("Erro ao cadastrar usuário:", error);
        document.querySelector("#signup-message").textContent = "Erro ao conectar com o servidor";
        document.querySelector("#signup-message").style.color = "red";
    }
});