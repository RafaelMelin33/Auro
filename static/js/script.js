const senhaCadastro = document.getElementById('senha');
const confirmaCadastro = document.getElementById('confirmaSenha');
const btnSubmit = document.getElementById('btnSubmit');

if (senhaCadastro && confirmaCadastro) {
    senhaCadastro.addEventListener('input', validaTudo);
    confirmaCadastro.addEventListener('input', validaTudo);
}

function validaTudo() {
    var senha = document.getElementById('senha').value;
    var confirmarSenha = document.getElementById('confirmaSenha').value;

    document.getElementById('minuscula').style.color = 'red';
    document.getElementById('maiuscula').style.color = 'red';
    document.getElementById('numero').style.color = 'red';
    document.getElementById('especial').style.color = 'red';
    document.getElementById('senhasNaoCoincidem').style.color = 'red';
    document.getElementById('senhasNaoCoincidem').innerText = '* Senhas não coincidem';
    document.getElementById('quantidade').style.color = 'red';

    // Atualiza indicadores de força
    for (let i = 0; i < senha.length; i++) {
        const c = senha[i];
        if (c >= 'a' && c <= 'z') {
            document.getElementById('minuscula').style.color = 'green';
        } else if (c >= 'A' && c <= 'Z') {
            document.getElementById('maiuscula').style.color = 'green';
        } else if (c >= '0' && c <= '9') {
            document.getElementById('numero').style.color = 'green';
        } else if ('!@#$%^&*()_+[]{}|:;,.<>?'.includes(c)) {
            document.getElementById('especial').style.color = 'green';
        }
    }

    if (senha.length >= 8) {
        document.getElementById('quantidade').style.color = 'green';
    }

    // Verifica coincidência
    if (senha && senha === confirmarSenha) {
        document.getElementById('senhasNaoCoincidem').style.color = 'green';
        document.getElementById('senhasNaoCoincidem').innerText = '* Senhas coincidem';
    }

    // Habilita botão se todos forem verdes
    if (document.getElementById('minuscula').style.color === 'green') {
        okMinuscula = true;
    }
    if (document.getElementById('maiuscula').style.color === 'green') {
        okMaiuscula = true;
    }
    if (document.getElementById('numero').style.color === 'green') {
        okNumero = true;
    }
    if (document.getElementById('especial').style.color === 'green') {
        okEspecial = true;
    }
    if (document.getElementById('senhasNaoCoincidem').style.color === 'green') {
        okCoincide = true;
    }
    if (document.getElementById('quantidade').style.color === 'green') {
        okQuantidade = true;
    }
    if (okMinuscula && okMaiuscula && okNumero && okEspecial && okCoincide && okQuantidade) {
        btnSubmit.disabled = false;
    } else {
        btnSubmit.disabled = true;
    }


    // const okMinuscula = document.getElementById('minuscula').style.color === 'green';
    // const okMaiuscula = document.getElementById('maiuscula').style.color === 'green';
    // const okNumero    = document.getElementById('numero').style.color === 'green';
    // const okEspecial  = document.getElementById('especial').style.color === 'green';
    // const okCoincide  = document.getElementById('senhasNaoCoincidem').style.color === 'green';
    // const okQuantidade = document.getElementById('quantidade').style.color === 'green';

    // btnSubmit.disabled = !(okMinuscula && okMaiuscula && okNumero && okEspecial && okCoincide && okQuantidade);
}

function verSenha() {
    var senhaInput = document.getElementById('senha');
    var olhoFechado = document.getElementById('olho_fechado_s');
    var olhoAberto = document.getElementById('olho_aberto_s');

    if (senhaInput.type === 'password') {
        senhaInput.type = 'text';
        olhoFechado.style.display = 'none';
        olhoAberto.style.display = 'inline';
    } else {
        senhaInput.type = 'password';
        olhoFechado.style.display = 'inline';
        olhoAberto.style.display = 'none';
    }
}

function verConfirmaSenha() {
    var confirmaSenhaInput = document.getElementById('confirmaSenha');
    var olhoFechado = document.getElementById('olho_fechado_cs');
    var olhoAberto = document.getElementById('olho_aberto_cs');

    if (confirmaSenhaInput.type === 'password') {
        confirmaSenhaInput.type = 'text';
        olhoFechado.style.display = 'none';
        olhoAberto.style.display = 'inline';
    } else {
        confirmaSenhaInput.type = 'password';
        olhoFechado.style.display = 'inline';
        olhoAberto.style.display = 'none';
    }
}

// Validação do nome
function validaEspaco() {
    if (document.getElementById('nome')) {
        valorInput = document.getElementById('nome')
    } else if (document.getElementById('descricao')) {
        valorInput = document.getElementById('descricao')
    }

    if (valorInput.value.startsWith(' ')) {
        valorInput.value = valorInput.value.trimStart();
    }
};

function validaEspacoSenha() {
    var senhaInput = document.getElementById('senha');
    if (senhaInput.value.startsWith(' ')) {
        senhaInput.value = senhaInput.value.trimStart();
    }
}

function validaEspacoConfirmaNome() {
    var confirmaNomeInput = document.getElementById('confirmaNome');
    if (confirmaNomeInput.value.startsWith(' ')) {
        confirmaNomeInput.value = confirmaNomeInput.value.trimStart();
    }
}

function validaEspacoEmail() {
    var valorInput = document.getElementById('email');
    if (valorInput.value.startsWith(' ')) {
        valorInput.value = valorInput.value.trimStart();
    }
}

function maiuscula(){
    var descricao = document.getElementById('descricao');
    descricao.value = descricao.value.toLowerCase();
    descricao.value = descricao.value.charAt(0).toUpperCase() + descricao.value.slice(1);
}

// --- Validação de senha no editar ---
const senhaInput = document.getElementById('senha');
const btnSalvar = document.getElementById('btnSalvar');

if (senhaInput) {
    // Campo senha existe: usuário comum, ativa validação
    senhaInput.addEventListener('input', validaTudoEditar);
    window.addEventListener('load', validaTudoEditar);
} else {
    // Não tem campo senha: admin, habilita botão salvar direto
    if (btnSalvar) btnSalvar.disabled = false;
}

function validaTudoEditar() {
    if (!senhaInput) return;

    const senha = senhaInput.value || '';

    // elementos dos critérios (devem existir no HTML)
    const minuscula = document.getElementById('minuscula');
    const maiuscula = document.getElementById('maiuscula');
    const numero = document.getElementById('numero');
    const especial = document.getElementById('especial');
    const quantidade = document.getElementById('quantidade');

    if (!minuscula || !maiuscula || !numero || !especial || !quantidade) return;

    // reset para vermelho (mesma lógica que você usou)
    minuscula.style.color = 'red';
    maiuscula.style.color = 'red';
    numero.style.color = 'red';
    especial.style.color = 'red';
    quantidade.style.color = 'red';

    // percorre caractere a caractere (mesma abordagem do cadastro)
    for (let i = 0; i < senha.length; i++) {
        const c = senha[i];
        if (c >= 'a' && c <= 'z') {
            minuscula.style.color = 'green';
        } else if (c >= 'A' && c <= 'Z') {
            maiuscula.style.color = 'green';
        } else if (c >= '0' && c <= '9') {
            numero.style.color = 'green';
        } else if ('!@#$%^&*()_+[]{}|:;,.<>?\\/~`-='.includes(c)) {
            especial.style.color = 'green';
        }
    }

    if (senha.length >= 8) {
        quantidade.style.color = 'green';
    }

    const okMinus = minuscula.style.color === 'green';
    const okMaius = maiuscula.style.color === 'green';
    const okNum = numero.style.color === 'green';
    const okEsp = especial.style.color === 'green';
    const okQuant = quantidade.style.color === 'green';

    // ativa/desativa botão (mesma lógica)
    if (btnSalvar) btnSalvar.disabled = !(okMinus && okMaius && okNum && okEsp && okQuant);
}

// liga o listener e executa no load (cobre campo já preenchido)
if (senhaInput) {
    senhaInput.addEventListener('input', validaTudoEditar);
    window.addEventListener('load', validaTudoEditar);
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

let mes = document.getElementById('pegaMes').value
console.log(mes)
document.getElementById('mes' + mes).style.backgroundColor = '#168C44';
document.getElementById('mes' + mes).style.color = 'white';