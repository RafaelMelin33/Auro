// Exibe a etapa 1 do formulário e esconde as demais
function irEtapa1() {
    document.getElementById("etapa1").style.display = 'flex'; // Mostra etapa 1
    document.getElementById("etapa2").style.display = 'none'; // Esconde etapa 2
    document.getElementById("etapa3").style.display = 'none'; // Esconde etapa 3
}

// Exibe a etapa 2 do formulário e esconde as demais
function irEtapa2() {
    document.getElementById("etapa1").style.display = 'none'; // Esconde etapa 1
    document.getElementById("etapa2").style.display = 'flex'; // Mostra etapa 2
    document.getElementById("etapa3").style.display = 'none'; // Esconde etapa 3
}

// Exibe a etapa 3 do formulário e esconde as demais
function irEtapa3() {
    document.getElementById("etapa1").style.display = 'none'; // Esconde etapa 1
    document.getElementById("etapa2").style.display = 'none'; // Esconde etapa 2
    document.getElementById("etapa3").style.display = 'flex'; // Mostra etapa 3
}

// Valida os requisitos da senha enquanto o usuário digita
document.getElementById('senha').addEventListener('input', function () {
    var senha = this.value; // Obtém o valor digitado
    // Inicialmente, todos os requisitos ficam vermelhos
    document.getElementById('minuscula').style.color = 'red';
    document.getElementById('maiuscula').style.color = 'red';
    document.getElementById('numero').style.color = 'red';
    document.getElementById('especial').style.color = 'red';
    // Percorre cada caractere da senha
    for (let i = 0; i < senha.length; i++) {
        const caractere = senha[i];
        // Se encontrar letra minúscula, muda cor para verde
        if (caractere >= 'a' && caractere <= 'z') {
            document.getElementById('minuscula').style.color = 'green';
            // Se encontrar letra maiúscula, muda cor para verde
        } else if (caractere >= 'A' && caractere <= 'Z') {
            document.getElementById('maiuscula').style.color = 'green';
            // Se encontrar número, muda cor para verde
        } else if (caractere >= '0' && caractere <= '9') {
            document.getElementById('numero').style.color = 'green';
            // Se encontrar caractere especial, muda cor para verde
        } else if ('!@#$%^&*()_+[]{}|;:,.<>?'.includes(caractere)) {
            document.getElementById('especial').style.color = 'green';
        }
    }
    senhasCoincidem(); // Chama função para verificar se as senhas coincidem
});

// Verifica se os campos de senha e confirmação são iguais
function senhasCoincidem() {
    var senha = document.getElementById('senha').value; // Valor da senha
    var confirmarSenha = document.getElementById('confirmaSenha').value; // Valor da confirmação
    document.getElementById('senhasNaoCoincidem').style.color = 'red'; // Inicialmente vermelho
    // Se as senhas forem iguais, muda cor para verde
    if (senha == confirmarSenha) {
        document.getElementById('senhasNaoCoincidem').style.color = 'green';
    }
}

// Alterna a visualização do campo de senha (mostrar/ocultar)
function verSenha() {
    var senhaInput = document.getElementById('senha'); // Campo senha
    var olhoFechado = document.getElementById('olho_fechado_s'); // Ícone olho fechado
    var olhoAberto = document.getElementById('olho_aberto_s'); // Ícone olho aberto

    // Se o campo está oculto, mostra a senha
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        olhoFechado.style.display = 'none';
        olhoAberto.style.display = 'inline';
        // Se o campo está visível, oculta a senha
    } else {
        senhaInput.type = 'password';
        olhoFechado.style.display = 'inline';
        olhoAberto.style.display = 'none';
    }
}

// Alterna a visualização do campo de confirmação de senha (mostrar/ocultar)
function verConfirmaSenha() {
    var confirmaSenhaInput = document.getElementById('confirmaSenha'); // Campo confirmação
    var olhoFechado = document.getElementById('olho_fechado_cs'); // Ícone olho fechado
    var olhoAberto = document.getElementById('olho_aberto_cs'); // Ícone olho aberto

    // Se o campo está oculto, mostra a senha
    if (confirmaSenhaInput.type === 'password') {
        confirmaSenhaInput.type = 'text';
        olhoFechado.style.display = 'none';
        olhoAberto.style.display = 'inline';
        // Se o campo está visível, oculta a senha
    } else {
        confirmaSenhaInput.type = 'password';
        olhoFechado.style.display = 'inline';
        olhoAberto.style.display = 'none';
    }
}

// Alterna o menu hamburguer entre aberto e fechado
function menu() {
    let aberto = 0 // Estado inicial do menu
    let btn = document.getElementById('menu_hamburguer'); // Botão do menu
    let nav = document.getElementById('nav'); // Elemento de navegação

    // Se o menu está fechado, abre
    if (aberto == 0 && nav.classList.contains('fechado')) {
        nav.classList.remove('fechado');
        nav.classList.add('aberto');
        btn.classList.remove('rodar2');
        btn.classList.add('rodar');
        aberto = 1;
        // Se o menu está aberto, fecha
    } else if (aberto == 0 && nav.classList.contains('aberto')) {
        nav.classList.remove('aberto');
        nav.classList.add('fechado');
        btn.classList.remove('rodar');
        btn.classList.add('rodar2');
        aberto = 0;
    }
}

// Alterna o menu do dashboard entre aberto e fechado
function menuDash() {
    let aberto = 0 // Estado inicial do menu
    let btn_dash = document.getElementById('menu_hamburguer_dash'); // Botão do menu dashboard
    let nav_dash = document.getElementById('nav_dash'); // Elemento de navegação dashboard

    // Se o menu está fechado, abre
    if (aberto == 0 && nav_dash.classList.contains('fechado')) {
        nav_dash.classList.remove('fechado');
        nav_dash.classList.add('aberto');
        btn_dash.classList.remove('rodar2');
        btn_dash.classList.add('rodar');
        aberto = 1;
        // Se o menu está aberto, fecha
    } else if (aberto == 0 && nav_dash.classList.contains('aberto')) {
        nav_dash.classList.remove('aberto');
        nav_dash.classList.add('fechado');
        btn_dash.classList.remove('rodar');
        btn_dash.classList.add('rodar2');
        aberto = 0;
    }
}
