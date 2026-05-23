document.addEventListener("DOMContentLoaded", async () => {
    let perguntas = [];

    try {
        const response = await fetch('/forms/questions');
        perguntas = await response.json();
    } catch (error) {
        console.error('Erro ao carregar perguntas:', error);
        // Fallback or error handling
        perguntas = [];
    }

    let perguntaAtual = 0;
    const respostas = {};

    const pagina = document.getElementById("questionario-page");
    const heroUrl = pagina.dataset.heroUrl;

    const passoAtual = document.getElementById("passo-atual");
    const perguntaTitulo = document.getElementById("pergunta-titulo");
    const opcoesContainer = document.getElementById("opcoes");
    const botaoVoltar = document.getElementById("botao-voltar");
    const botaoProximo = document.getElementById("botao-proximo");
    const formulario = document.getElementById("questionario-form");
    const progressoContainer = document.getElementById("progresso");

    // Generate progress bars dynamically
    progressoContainer.innerHTML = '';
    for (let i = 0; i < perguntas.length; i++) {
        const span = document.createElement('span');
        progressoContainer.appendChild(span);
    }
    const barrasProgresso = Array.from(progressoContainer.querySelectorAll('span'));

    const modalOverlay = document.getElementById("modal-overlay");
    const modalLabel = document.getElementById("modal-label");
    const modalTitulo = document.getElementById("modal-titulo");
    const modalTexto = document.getElementById("modal-texto");
    const modalCancelar = document.getElementById("modal-cancelar");
    const modalConfirmar = document.getElementById("modal-confirmar");

    let acaoConfirmarModal = null;
    let acaoCancelarModal = null;

    function abrirModal({
        label = "AVISO",
        titulo = "",
        texto = "",
        textoConfirmar = "OK",
        textoCancelar = "Cancelar",
        mostrarCancelar = true,
        onConfirm = null,
        onCancel = null
    }) {
        modalLabel.textContent = label;
        modalTitulo.textContent = titulo;
        modalTexto.textContent = texto;
        modalConfirmar.textContent = textoConfirmar;
        modalCancelar.textContent = textoCancelar;

        acaoConfirmarModal = onConfirm;
        acaoCancelarModal = onCancel;

        modalCancelar.style.display = mostrarCancelar ? "inline-flex" : "none";
        modalOverlay.classList.add("ativo");
    }

    function fecharModal() {
        modalOverlay.classList.remove("ativo");
        acaoConfirmarModal = null;
        acaoCancelarModal = null;
    }

    modalConfirmar.addEventListener("click", () => {
        if (acaoConfirmarModal) {
            acaoConfirmarModal();
        } else {
            fecharModal();
        }
    });

    modalCancelar.addEventListener("click", () => {
        if (acaoCancelarModal) {
            acaoCancelarModal();
        }
        fecharModal();
    });

    modalOverlay.addEventListener("click", (event) => {
        if (event.target === modalOverlay) {
            fecharModal();
        }
    });

    function renderizarPergunta() {
        if (perguntas.length === 0) {
            perguntaTitulo.textContent = "Erro ao carregar perguntas.";
            return;
        }

        const pergunta = perguntas[perguntaAtual];
        const respostaAtual = respostas[pergunta.id];

        passoAtual.textContent = `Pergunta ${perguntaAtual + 1} de ${perguntas.length}`;
        perguntaTitulo.textContent = pergunta.question;

        if (pergunta.type === "scale") {
            const labels = ["Discordo totalmente", "Discordo", "Neutro", "Concordo", "Concordo totalmente"];
            opcoesContainer.innerHTML = labels.map((label, index) => {
                const value = index + 1;
                return `
                    <label class="opcao">
                        <input type="radio" name="resposta" value="${value}" ${respostaAtual == value ? "checked" : ""}>
                        <span class="opcao-card">
                            <strong>${value} - ${label}</strong>
                        </span>
                    </label>
                `;
            }).join("");
        } else {
            // Fallback for other types
            opcoesContainer.innerHTML = "<p>Tipo de pergunta não suportado.</p>";
        }

        barrasProgresso.forEach((barra, indice) => {
            barra.className = "";

            if (indice < perguntaAtual) {
                barra.classList.add("feito");
            } else if (indice === perguntaAtual) {
                barra.classList.add("atual");
            }
        });

        botaoVoltar.textContent = perguntaAtual === 0 ? "SAIR" : "VOLTAR";
        botaoProximo.textContent = perguntaAtual === perguntas.length - 1 ? "SALVAR E ENVIAR" : "PRÓXIMO";
    }

    opcoesContainer.addEventListener("change", (event) => {
        if (event.target.name === "resposta") {
            const pergunta = perguntas[perguntaAtual];
            respostas[pergunta.id] = parseInt(event.target.value);
        }
    });

    botaoVoltar.addEventListener("click", () => {
        if (perguntaAtual === 0) {
            window.location.href = heroUrl;
            return;
        }

        perguntaAtual -= 1;
        renderizarPergunta();
    });

    formulario.addEventListener("submit", (event) => {
        event.preventDefault();

        const selecionada = formulario.querySelector('input[name="resposta"]:checked');

        if (!selecionada) {
            abrirModal({
                label: "ATENÇÃO",
                titulo: "Selecione uma resposta",
                texto: "Você precisa escolher uma opção antes de continuar.",
                textoConfirmar: "Entendi",
                mostrarCancelar: false,
                onConfirm: fecharModal
            });
            return;
        }

        const pergunta = perguntas[perguntaAtual];
        respostas[pergunta.id] = parseInt(selecionada.value);

        if (perguntaAtual === perguntas.length - 1) {
            abrirModal({
                label: "FINALIZAR QUESTIONÁRIO",
                titulo: "Deseja salvar e enviar suas respostas?",
                texto: "Se confirmar, os dados serão salvos e enviados para as psicólogas da empresa.",
                textoConfirmar: "Salvar e enviar",
                textoCancelar: "Revisar",
                mostrarCancelar: true,
                onConfirm: async () => {
                    try {
                        const answers = perguntas.map(pergunta => ({
                            question_id: pergunta.id,
                            value: respostas[pergunta.id] || 0
                        }));
                        const payload = {
                            user_id: 1, // TODO: get from session or input
                            answers: answers,
                            created_at: new Date().toISOString()
                        };
                        const response = await fetch('/forms/submit', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(payload)
                        });
                        if (response.ok) {
                            abrirModal({
                                label: "DADOS ENVIADOS",
                                titulo: "Respostas enviadas com sucesso",
                                texto: "Os dados foram salvos e enviados para as psicólogas da empresa.",
                                textoConfirmar: "Voltar ao painel",
                                mostrarCancelar: false,
                                onConfirm: () => {
                                    window.location.href = heroUrl;
                                }
                            });
                        } else {
                            throw new Error('Erro no envio');
                        }
                    } catch (error) {
                        console.error('Erro ao enviar:', error);
                        abrirModal({
                            label: "ERRO",
                            titulo: "Erro ao enviar respostas",
                            texto: "Ocorreu um erro ao enviar suas respostas. Tente novamente.",
                            textoConfirmar: "OK",
                            mostrarCancelar: false,
                            onConfirm: fecharModal
                        });
                    }
                }
            });
            return;
        }

        perguntaAtual += 1;
        renderizarPergunta();
    });

    renderizarPergunta();
});
