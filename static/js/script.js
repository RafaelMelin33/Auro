function irEtapa1() {
    document.getElementById("etapa1").style.display = 'flex';
    document.getElementById("etapa2").style.display = 'none';
    document.getElementById("etapa3").style.display = 'none';
}

function irEtapa2() {
    document.getElementById("etapa1").style.display = 'none';
    document.getElementById("etapa2").style.display = 'flex';
    document.getElementById("etapa3").style.display = 'none';
}

function irEtapa3() {
    document.getElementById("etapa1").style.display = 'none';
    document.getElementById("etapa2").style.display = 'none';
    document.getElementById("etapa3").style.display = 'flex';
}

document.getElementById('senha').addEventListener('input', function () {
    var senha = this.value;
    document.getElementById('minuscula').style.color = 'red';
    document.getElementById('maiuscula').style.color = 'red';
    document.getElementById('numero').style.color = 'red';
    document.getElementById('especial').style.color = 'red';
    for (let i = 0; i < senha.length; i++) {
        const caractere = senha[i];
        if (caractere >= 'a' && caractere <= 'z') {
            document.getElementById('minuscula').style.color = 'green';
        } else if (caractere >= 'A' && caractere <= 'Z') {
            document.getElementById('maiuscula').style.color = 'green';
        } else if (caractere >= '0' && caractere <= '9') {
            document.getElementById('numero').style.color = 'green';
        } else if ('!@#$%^&*()_+[]{}|;:,.<>?'.includes(caractere)) {
            document.getElementById('especial').style.color = 'green';
        }    
    }
});

document.getElementById('confirmaSenha').addEventListener('input', function () {
    var senha = document.getElementById('senha').value;
    var confirmarSenha = this.value;
    document.getElementById('senhasNaoCoincidem').style.color = 'red';
    if (senha == confirmarSenha) {
        document.getElementById('senhasNaoCoincidem').style.color = 'green';
    }
});