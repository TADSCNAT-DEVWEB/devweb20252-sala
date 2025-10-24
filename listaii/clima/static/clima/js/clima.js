// Buscador de Clima - JavaScript
// Elementos DOM
const cidadeInput = document.getElementById('cidadeInput');
const buscarBtn = document.getElementById('buscarBtn');
const loadingBox = document.getElementById('loadingBox');
const resultadoBox = document.getElementById('resultadoBox');
const erroBox = document.getElementById('erroBox');

// Elementos de resultado
const nomeCidade = document.getElementById('nomeCidade');
const temperatura = document.getElementById('temperatura');
const descricao = document.getElementById('descricao');
const climaIcon = document.getElementById('climaIcon');
const mensagemErro = document.getElementById('mensagemErro');

// Event listeners
buscarBtn.addEventListener('click', buscarClima);
cidadeInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        buscarClima();
    }
});

// Função principal de busca
function buscarClima() {
    const cidade = cidadeInput.value.trim();
    
    if (!cidade) {
        mostrarErro('Por favor, digite o nome de uma cidade.');
        return;
    }

    // Mostrar loading e esconder outros elementos
    mostrarLoading()
        .then(() => {
            const urlClima = document.getElementById('url_clima').dataset.url;

            return fetch(`${urlClima}?nome_cidade=${encodeURIComponent(cidade)}`);
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                mostrarResultado(data);
            } else {
                mostrarErro(data.erro || 'Cidade não encontrada.');
            }
        })
        .catch(error => {
            console.error('Erro na requisição:', error);
            mostrarErro('Erro de conexão. Tente novamente.');
        });
}

// Mostrar loading
function mostrarLoading() {
    esconderTodos();
    loadingBox.style.display = 'block';
    
    // Pequeno delay para garantir que o loading seja visível
    return new Promise(resolve => {
        setTimeout(resolve, 500); // 500ms de delay
    });
}

// Mostrar resultado
function mostrarResultado(data) {
    esconderTodos();
    
    nomeCidade.textContent = data.nome_cidade;
    temperatura.textContent = data.temperatura;
    descricao.textContent = data.descricao;
    
    // Definir ícone baseado na descrição
    definirIconeClima(data.descricao);
    
    resultadoBox.style.display = 'block';
}

// Mostrar erro
function mostrarErro(mensagem) {
    esconderTodos();
    mensagemErro.textContent = mensagem;
    erroBox.style.display = 'block';
}

// Esconder todos os elementos de resultado
function esconderTodos() {
    loadingBox.style.display = 'none';
    resultadoBox.style.display = 'none';
    erroBox.style.display = 'none';
}

// Definir ícone do clima
function definirIconeClima(descricaoClima) {
    const desc = descricaoClima.toLowerCase();
    let iconClass = 'fas fa-eye';
    
    if (desc.includes('sol') || desc.includes('ensolarado')) {
        iconClass = 'fas fa-sun';
    } else if (desc.includes('chuva') || desc.includes('chuvoso')) {
        iconClass = 'fas fa-cloud-rain';
    } else if (desc.includes('nublado') || desc.includes('nuvem')) {
        iconClass = 'fas fa-cloud';
    } else if (desc.includes('neve')) {
        iconClass = 'fas fa-snowflake';
    } else if (desc.includes('tempestade')) {
        iconClass = 'fas fa-bolt';
    }
    
    climaIcon.className = iconClass;
}

// Nova consulta
function novaConsulta() {
    esconderTodos();
    cidadeInput.value = '';
    cidadeInput.focus();
}

// Fechar erro
function fecharErro() {
    erroBox.style.display = 'none';
}

// Focus inicial no input
window.addEventListener('load', function() {
    cidadeInput.focus();
});