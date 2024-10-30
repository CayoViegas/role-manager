const BASE_URL = "http://localhost:5000";

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
                Authorization: `Bearer ${token}`,
            },
        });

        // Se a resposta for 404, significa que não há personagens cadastrados
        if (response.status === 404) {
            document.querySelector("#error-message").textContent = "Nenhum personagem cadastrado";
            document.querySelector("#username").textContent = localStorage.getItem("username");
            return;
        }

        if (!response.ok) {
            document.querySelector("#error-message").textContent =
                "Erro ao buscar personagens";
            return;
        }

        const characters = await response.json();

        // Definir o nome do usuário
        document.querySelector("#username").textContent =
            localStorage.getItem("username");

        // Exibir os personagens na tela
        const container = document.querySelector("#characters-container");
        container.innerHTML = ""; // Limpar qualquer conteúdo anterior

        characters.forEach((character) => {
            const ownerInfo = character.owner
                ? `<p>Dono: ${character.owner}</p>`
                : ""; // Verifica se o dono está disponível

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
    localStorage.removeItem("userId");
    window.location.href = "index.html";
}

// Chamar a função assim que a página carregar
window.addEventListener("DOMContentLoaded", getCharacters);

// Adicionar o evento de clique no botão de logout
document.querySelector("#logout-button").addEventListener("click", logout);

// Selecionar o modal e o botão de criar personagem
const createCharacterModal = document.getElementById("create-character-modal");
const createCharacterButton = document.getElementById("create-character-button");
const closeButton = document.querySelector(".close-button");

// Função para abrir o modal
function openModal() {
    createCharacterModal.style.display = "block";
}

// Função para fechar o modal
function closeModal() {
    createCharacterModal.style.display = "none";
}

// Eventos para abrir e fechar o modal
createCharacterButton.addEventListener("click", openModal);
closeButton.addEventListener("click", closeModal);

// Evento para fechar o modal se o usuário clicar fora dele
window.addEventListener("click", (event) => {
    if (event.target === createCharacterModal) {
        closeModal();
    }
});

// Função para criar um novo personagem
async function createCharacter(event) {
    event.preventDefault(); // Impedir o envio padrão do formulário

    const token = localStorage.getItem("token");
    const name = document.getElementById("character-name").value;
    const race = document.getElementById("character-race").value;
    const class_ = document.getElementById("character-class").value;
    const level = parseInt(document.getElementById("character-level").value, 10);

    try {
        const response = await fetch(BASE_URL + "/characters", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                name,
                race,
                class_: class_,
                level,
            }),
        });

        if (response.status === 201) {
            // Personagem criado com sucesso
            closeModal();
            getCharacters(); // Atualizar a lista de personagens
        } else {
            // Erro ao criar personagem
            document.querySelector("#error-message").textContent =
                "Erro ao criar personagem";
        }
    } catch (error) {
        console.error("Erro ao criar personagem", error);
    }
}

// Adicionar o evento de submit no formulário de criação de personagem
document.getElementById("create-character-form").addEventListener("submit", createCharacter);

// Selecionar o modal e os botões do modal de exclusão
const deleteUserModal = document.getElementById("delete-user-modal");
const deleteUserButton = document.getElementById("delete-user-button");
const closeModalButton = document.querySelector(".close-button");
const confirmDeleteButton = document.getElementById("confirm-delete-user");
const cancelDeleteButton = document.getElementById("cancel-delete-user");

// Função para abrir o modal de confirmação de exclusão
function openDeleteUserModal() {
    deleteUserModal.style.display = "block";
}

// Função para fechar o modal de confirmação de exclusão
function closeDeleteUserModal() {
    deleteUserModal.style.display = "none";
}

// Evento para abrir o modal de confirmação de exclusão ao clicar no botão de exclusão
deleteUserButton.addEventListener("click", openDeleteUserModal);

// Eventos para fechar o modal de confirmação de exclusão
closeModalButton.addEventListener("click", closeDeleteUserModal);
cancelDeleteButton.addEventListener("click", closeDeleteUserModal);

// Evento para fechar o modal de confirmação de exclusão se o usuário clicar fora dele
window.addEventListener("click", (event) => {
    if (event.target === deleteUserModal) {
        closeDeleteUserModal();
    }
});

// Função para deletar o usuário
async function deleteUser() {
    const token = localStorage.getItem("token");
    const userId = localStorage.getItem("userId");

    if (!token || !userId) {
        console.error("Usuário não autenticado ou ID do usuário não encontrado");
        return;
    }

    try {
        const response = await fetch(BASE_URL + "/users/" + userId, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
            alert("Usuário deletado com sucesso.");
            // Limpar o localStorage e redirecionar para a página de login
            localStorage.removeItem("token");
            localStorage.removeItem("username");
            localStorage.removeItem("userId");
            window.location.href = "index.html";
        } else {
            alert("Erro ao deletar usuário");
        }
    } catch (error) {
        console.error("Erro ao deletar usuário", error);
        alert("Erro ao conectar com o servidor");
    }
}

// Evento para confirmar a exclusão do usuário
confirmDeleteButton.addEventListener("click", () => {
    deleteUser();
    closeDeleteUserModal();
});