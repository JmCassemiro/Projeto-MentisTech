document.addEventListener("DOMContentLoaded", () => {
    const perguntas = [
        {
            titulo: "Como você está se sentindo hoje?",
            opcoes: [
                { valor: "feliz", rotulo: "Feliz", emoji: ":)" },
                { valor: "neutro", rotulo: "Neutro", emoji: ":|" },
                { valor: "triste", rotulo: "Triste", emoji: ":(" },
                { valor: "estressado", rotulo: "Estressado", emoji: ">:(" }
            ]
        },
        {
            titulo: "Como está seu nível de energia agora?",
            opcoes: [
                { valor: "muito_alta", rotulo: "Muito alta", emoji: ":D" },
                { valor: "boa", rotulo: "Boa", emoji: ":)" },
                { valor: "baixa", rotulo: "Baixa", emoji: ":/" },
                { valor: "muito_baixa", rotulo: "Muito baixa", emoji: ":(" }
            ]
        },
        {
            titulo: "Como foi sua qualidade de sono recentemente?",
            opcoes: [
                { valor: "otima", rotulo: "Ótima", emoji: ":)" },
                { valor: "regular", rotulo: "Regular", emoji: ":|" },
                { valor: "ruim", rotulo: "Ruim", emoji: ":/" },
                { valor: "muito_ruim", rotulo: "Muito ruim", emoji: ":(" }
            ]
        },
        {
            titulo: "Como você percebe seu nível de estresse hoje?",
            opcoes: [
                { valor: "baixo", rotulo: "Baixo", emoji: ":)" },
                { valor: "medio", rotulo: "Médio", emoji: ":|" },
                { valor: "alto", rotulo: "Alto", emoji: ":/" },
                { valor: "muito_alto", rotulo: "Muito alto", emoji: ">:(" }
            ]
        },
        {
            titulo: "Como está sua concentração nas tarefas?",
            opcoes: [
                { valor: "excelente", rotulo: "Excelente", emoji: ":D" },
                { valor: "boa", rotulo: "Boa", emoji: ":)" },
                { valor: "instavel", rotulo: "Instável", emoji: ":/" },
                { valor: "dificil", rotulo: "Muito difícil", emoji: ":(" }
            ]
        },
        {
            titulo: "Como você descreveria seu bem-estar geral hoje?",
            opcoes: [
                { valor: "muito_bem", rotulo: "Muito bem", emoji: ":D" },
                { valor: "bem", rotulo: "Bem", emoji: ":)" },
                { valor: "mais_ou_menos", rotulo: "Mais ou menos", emoji: ":|" },
                { valor: "mal", rotulo: "Mal", emoji: ":(" }
            ]
        }
    ];

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
    const barrasProgresso = Array.from(document.querySelectorAll("#progresso span"));

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
        const pergunta = perguntas[perguntaAtual];
        const respostaAtual = respostas[perguntaAtual];

        passoAtual.textContent = `Pergunta ${perguntaAtual + 1} de ${perguntas.length}`;
        perguntaTitulo.textContent = pergunta.titulo;

        opcoesContainer.innerHTML = pergunta.opcoes.map((opcao) => `
            <label class="opcao">
                <input type="radio" name="resposta" value="${opcao.valor}" ${respostaAtual === opcao.valor ? "checked" : ""}>
                <span class="opcao-card">
                    <span class="emoji">${opcao.emoji}</span>
                    <strong>${opcao.rotulo}</strong>
                </span>
            </label>
        `).join("");

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
            respostas[perguntaAtual] = event.target.value;
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

        respostas[perguntaAtual] = selecionada.value;

        if (perguntaAtual === perguntas.length - 1) {
            abrirModal({
                label: "FINALIZAR QUESTIONÁRIO",
                titulo: "Deseja salvar e enviar suas respostas?",
                texto: "Se confirmar, os dados serão salvos e enviados para as psicólogas da empresa.",
                textoConfirmar: "Salvar e enviar",
                textoCancelar: "Revisar",
                mostrarCancelar: true,
                onConfirm: () => {
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
                }
            });
            return;
        }

        perguntaAtual += 1;
        renderizarPergunta();
    });

    renderizarPergunta();
});
