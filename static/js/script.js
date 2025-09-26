// Função para exibir a etapa 1 e ocultar as demais
function irEtapa1() {
    // Exibe o elemento com id 'etapa1' usando display flex
    document.getElementById("etapa1").style.display = 'flex';
    // Oculta o elemento com id 'etapa2'
    document.getElementById("etapa2").style.display = 'none';
    // Oculta o elemento com id 'etapa3'
    document.getElementById("etapa3").style.display = 'none';
}

// Função para exibir a etapa 2 e ocultar as demais
function irEtapa2() {
    // Oculta o elemento com id 'etapa1'
    document.getElementById("etapa1").style.display = 'none';
    // Exibe o elemento com id 'etapa2' usando display flex
    document.getElementById("etapa2").style.display = 'flex';
    // Oculta o elemento com id 'etapa3'
    document.getElementById("etapa3").style.display = 'none';
}

// Função para exibir a etapa 3 e ocultar as demais
function irEtapa3() {
    // Oculta o elemento com id 'etapa1'
    document.getElementById("etapa1").style.display = 'none';
    // Oculta o elemento com id 'etapa2'
    document.getElementById("etapa2").style.display = 'none';
    // Exibe o elemento com id 'etapa3' usando display flex
    document.getElementById("etapa3").style.display = 'flex';
}

// Validação dinâmica da senha: verifica se contém minúscula, maiúscula, número e caractere especial
document.getElementById('senha').addEventListener('input',function () {
    // Pega o valor digitado no campo senha
    var senha = this.value;
    // Inicialmente, todos os requisitos ficam vermelhos
    document.getElementById('minuscula').style.color = 'red'; // Requisito de minúscula
    document.getElementById('maiuscula').style.color = 'red'; // Requisito de maiúscula
    document.getElementById('numero').style.color = 'red';    // Requisito de número
    document.getElementById('especial').style.color = 'red';  // Requisito de caractere especial
    // Percorre cada caractere da senha e valida os requisitos
    for (let i = 0; i < senha.length; i++) {
        const caractere = senha[i]; // Pega o caractere atual
        // Se for minúscula, muda cor do requisito para verde
        if (caractere >= 'a' && caractere <= 'z') {
            document.getElementById('minuscula').style.color = 'green';
        // Se for maiúscula, muda cor do requisito para verde
        } else if (caractere >= 'A' && caractere <= 'Z') {
            document.getElementById('maiuscula').style.color = 'green';
        // Se for número, muda cor do requisito para verde
        } else if (caractere >= '0' && caractere <= '9') {
            document.getElementById('numero').style.color = 'green';
        // Se for caractere especial, muda cor do requisito para verde
        } else if ('!@#$%^&*()_+[]{}|;:,.<>?'.includes(caractere)) {
            document.getElementById('especial').style.color = 'green';
        }
    }
    // Chama função para verificar se as senhas coincidem
    senhasCoincidem();
});

// Função para verificar se os campos de senha e confirmação de senha são iguais
function senhasCoincidem() {
    // Pega o valor do campo senha
    var senha = document.getElementById('senha').value;
    // Pega o valor do campo confirmação de senha
    var confirmarSenha = document.getElementById('confirmaSenha').value;
    // Por padrão, mostra mensagem de erro em vermelho
    document.getElementById('senhasNaoCoincidem').style.color = 'red';
    // Se as senhas forem iguais, muda a cor para verde
    if (senha == confirmarSenha) {
        document.getElementById('senhasNaoCoincidem').style.color = 'green';
    }
}

// Alterna a visualização da senha (mostrar/ocultar)
function verSenha() {
    // Pega o input da senha
    var senhaInput = document.getElementById('senha');
    // Pega o ícone de olho fechado
    var olhoFechado = document.getElementById('olho_fechado_s');
    // Pega o ícone de olho aberto
    var olhoAberto = document.getElementById('olho_aberto_s');

    // Se o tipo do input for password, mostra a senha
    if (senhaInput.type === 'password') {
        senhaInput.type = 'text'; // Troca para texto
        olhoFechado.style.display = 'none'; // Esconde o olho fechado
        olhoAberto.style.display = 'inline'; // Mostra o olho aberto
    } else {
        // Se já estiver mostrando, volta para password
        senhaInput.type = 'password';
        olhoFechado.style.display = 'inline'; // Mostra o olho fechado
        olhoAberto.style.display = 'none'; // Esconde o olho aberto
    }
}

// Alterna a visualização da confirmação de senha (mostrar/ocultar)
function verConfirmaSenha() {
    // Pega o input de confirmação de senha
    var confirmaSenhaInput = document.getElementById('confirmaSenha');
    // Pega o ícone de olho fechado
    var olhoFechado = document.getElementById('olho_fechado_cs');
    // Pega o ícone de olho aberto
    var olhoAberto = document.getElementById('olho_aberto_cs');

    // Se o tipo do input for password, mostra a senha
    if (confirmaSenhaInput.type === 'password') {
        confirmaSenhaInput.type = 'text'; // Troca para texto
        olhoFechado.style.display = 'none'; // Esconde o olho fechado
        olhoAberto.style.display = 'inline'; // Mostra o olho aberto
    } else {
        // Se já estiver mostrando, volta para password
        confirmaSenhaInput.type = 'password';
        olhoFechado.style.display = 'inline'; // Mostra o olho fechado
        olhoAberto.style.display = 'none'; // Esconde o olho aberto
    }
}


// Função para alternar o menu hamburguer (abrir/fechar menu principal)
function menu() {
    let aberto = 0 // Variável para controlar o estado do menu (não é persistente entre execuções)
    let btn = document.getElementById('menu_hamburguer'); // Botão do menu hamburguer
    let nav = document.getElementById('nav'); // Elemento de navegação principal

    // Se o menu está fechado, abre o menu
    if (aberto == 0 && nav.classList.contains('fechado')) {
        nav.classList.remove('fechado'); // Remove classe de fechado
        nav.classList.add('aberto');     // Adiciona classe de aberto
        btn.classList.remove('rodar2'); // Remove animação de fechar
        btn.classList.add('rodar');     // Adiciona animação de abrir
        aberto = 1;                     // Marca como aberto
    // Se o menu está aberto, fecha o menu
    } else if (aberto == 0 && nav.classList.contains('aberto')) {
        nav.classList.remove('aberto'); // Remove classe de aberto
        nav.classList.add('fechado');   // Adiciona classe de fechado
        btn.classList.remove('rodar');  // Remove animação de abrir
        btn.classList.add('rodar2');    // Adiciona animação de fechar
        aberto = 0;                     // Marca como fechado
    }
}

// Função para alternar o menu hamburguer do dashboard (abrir/fechar menu lateral)
function menuDash() {
    let aberto = 0 // Variável para controlar o estado do menu (não é persistente entre execuções)
    let btn = document.getElementById('menu_hamburguer_dash'); // Botão do menu hamburguer do dashboard
    let nav = document.getElementById('nav_dash'); // Elemento de navegação do dashboard

    // Se o menu está fechado, abre o menu
    if (aberto == 0 && nav.classList.contains('fechado')) {
        nav.classList.remove('fechado'); // Remove classe de fechado
        nav.classList.add('aberto');     // Adiciona classe de aberto
        btn.classList.remove('rodar2'); // Remove animação de fechar
        btn.classList.add('rodar');     // Adiciona animação de abrir
        aberto = 1;                     // Marca como aberto
    // Se o menu está aberto, fecha o menu
    } else if (aberto == 0 && nav.classList.contains('aberto')) {
        nav.classList.remove('aberto'); // Remove classe de aberto
        nav.classList.add('fechado');   // Adiciona classe de fechado
        btn.classList.remove('rodar');  // Remove animação de abrir
        btn.classList.add('rodar2');    // Adiciona animação de fechar
        aberto = 0;                     // Marca como fechado
    }
}
