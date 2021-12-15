    function escolher() {
    var numSele = document.getElementById('sele')
    let resultado = document.getElementById('res')
    let entrada = Number(numSele.value)

    if ( entrada <= 0 ) {
        alert(`Impossível contar`)
    } //else {
        //resultado.innerHTML = `Contando: <br>`
    //}
    if ( entrada==1 ) {
        let Lq = prompt(`Qual é o valor de um dos LADOS do quadrado?`)
        let R1 = Lq ** 2
        resultado.innerHTML = `A área do quadrado é <strong>${R1}</strong>`
    }
    if ( entrada==2 ) {
        let Bt = prompt(`Qual é o valor da BASE do triângulo?`)
        let Ht = prompt(`Qual é o valor da ALTURA do triângulo?`)
        let R2 = Bt * Ht / 2
        resultado.innerHTML = `A área do triângulo é <strong>${R2}</strong>`
    }
    if ( entrada==3 ) {
        let Dl = prompt(`Qual o valor do DIAMETRO MAIOR?`)
        let dl = prompt(`Qual o valor do DIAMETRO MENOR`)
        let R3 = Dl * dl / 2
        resultado.innerHTML = `A área do losango é <strong>${R3}</strong>`
    }
    if ( entrada==4 ) {
        let Br = prompt(`Qual o valor da BASE do retângulo`)
        let Ar = prompt(`Qual o valor da ALTURA do retângulo`)
        let R4 = Br * Ar
        resultado.innerHTML = `A área do retângulo é <strong>${R4}</strong>`
    }
    if ( entrada==5 ) {
        let Pi = prompt(`Qual o valor de PI?`)
        let Ra = prompt(`Qual o valor do RAIO do círculo?`)
        let R5 = Pi * (Ra ** 2)
        resultado.innerHTML = `A área do círculo é <strong>${R5}</strong>`
    }
    if ( entrada==6 ) {
        let Btra = Number(window.prompt(`Qual o valor da BASE MAIOR do trapézio?`)) // Pode ser com ou sem o window
        let btra = Number(prompt(`Qual o valor da BASE MENOR do trapézio?`))
        Atra = prompt(`Qual o valor da ALTURA do trapézio?`)

        let R6 = (Btra + btra) * Atra / 2
        resultado.innerHTML = `A área do trapézio é <strong>${R6}</strong>`
    }
    if ( entrada >= 7 ) {
        window.alert(`Valor inválido!! Digite de acordo com as opções.`)
    }
}