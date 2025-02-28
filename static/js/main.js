document.addEventListener("DOMContentLoaded", function () {
    // Remover apenas alertas de mensagens flash, mantendo a última despesa visível
    setTimeout(() => {
        document.querySelectorAll(".alert").forEach(alert => {
            // Somente remove alertas que não contenham "Última despesa"
            if (!alert.textContent.includes("Última despesa")) {
                alert.style.transition = "opacity 0.5s";
                alert.style.opacity = "0";
                setTimeout(() => alert.remove(), 500);
            }
        });
    }, 3000);
});

    // Botão de adicionar orçamento com animação
    const expenseForm = document.getElementById("expense-form");
    const submitButton = expenseForm.querySelector("button");

    expenseForm.addEventListener("submit", function () {
        submitButton.innerHTML = "Adicionando...";
        submitButton.disabled = true;

        setTimeout(() => {
            submitButton.innerHTML = "Adicionar";
            submitButton.disabled = false;
        }, 1500);
    });

    // Adicionar efeito de hover aos botões da tabela
    document.addEventListener("mouseover", function (event) {
        if (event.target.classList.contains("btn")) {
            event.target.style.transform = "scale(1.1)";
            event.target.style.transition = "transform 0.2s";
        }
    });

    document.addEventListener("mouseout", function (event) {
        if (event.target.classList.contains("btn")) {
            event.target.style.transform = "scale(1)";
        }
    });

    // Animação ao remover uma despesa
    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-expense")) {
            const row = event.target.closest("tr");
            row.style.transition = "opacity 0.5s";
            row.style.opacity = "0";
            setTimeout(() => row.remove(), 500);
        }
    });
