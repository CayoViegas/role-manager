BASE_URL = "http://localhost:5000";

// Função para obter os personagens e exibir na tela
async function getCharacters() {
    const token = localStorage.getItem("token");

    if (!token) {
        window.location.href = "index.html"; // Redireciona se não houver token
        return;
    }

    try {
        // Fazer a requisição para buscar o nome do usuário e os personagens
        const response = await fetch(BASE_URL + "/characters", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            console.error("Erro ao buscar personagens");
            return;
        }

        const characters = await response.json();

        // Definir o nome do usuário
        document.querySelector("#username").textContent = localStorage.getItem("username");

        // Exibir os personagens na tela
        const container = document.querySelector("#characters-container");
        container.innerHTML = ""; // Limpar qualquer conteúdo anterior

        characters.forEach((character) => {
            const ownerInfo = character.owner ? `<p>Dono: ${character.owner}</p>` : ""; // Verifica se o dono está disponível

            const card = `
                <div class="character-card">
                    <h2>${character.name}</h2>
                    <p>Raça: ${character.race}</p>
                    <p>Classe: ${character.class}</p>
                    <p>Nível: ${character.level}</p>
                    ${ownerInfo} <!-- Exibir o nome do dono se disponível -->
                </div>
            `;
            container.innerHTML += card;
        });
    } catch (error) {
        console.error("Erro ao buscar personagens", error);
    }
}

// Função para deslogar o usuário
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "index.html";
}

// Chamar a função assim que a página carregar
window.addEventListener("DOMContentLoaded", getCharacters);

// Adicionar o evento de clique no botão de logout
document.querySelector("#logout-button").addEventListener("click", logout);