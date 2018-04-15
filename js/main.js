var numeroDeLinhas = 8;
var numeroDeColunas = 8;
var posicaoAtual = [7, 4]; // posição inicial da peça
var jogadaTentada = false;
var debug = false;

var casas = populaTabuleiro(numeroDeLinhas, numeroDeColunas);
criaPeca(casas, posicaoAtual);

function gameLoop() {
  criaPossibilidades(casas, posicaoAtual);
  $(movePeca(casas));
}

setInterval(gameLoop, 50);

function populaTabuleiro(numeroDeLinhas, numeroDeColunas){
  var tabuleiro = $("#tabuleiro"); // o $ em jQuery é o mesmo que document.querySelector
                                  // ou seja, pega a table do html cujo id é tabuleiro
  var casas = new Array();

  for (var i = 0; i < numeroDeLinhas; i++){
    casas[i] = new Array();
    var linha = $("<tr>"); // o $ também serve como criador de novos elementos
                          // nesse caso estamos criando uma nova tr (table record)
    tabuleiro.append(linha); // como tabuleiro é uma tabela, ela pode incluir table records filhos
                            // que é o que a função append faz

    for (var j = 0;j < numeroDeColunas; j++){
      casas[i][j] = $("<td>"); // criando um td (table data), ou seja, uma coluna de uma linha
                              // daquela tabela
      pintaCasa(casas[i][j], i, j);
      linha.append(casas[i][j]); // cada linha vai ter certa quantidade de colunas
    }
  }

  return casas;
}

function pintaCasa(casa, i, j){
  if ((i + j) % 2 == 0){
    casa.addClass("casa-preta"); // como todo o projeto é interpretado em tempo de execução pelo
                                // navegador, adicionando a classe "casa-preta" ao DOM casa, que é
                                // um td, fará com que ele herde as características descritas por
                                // "casa-preta" no index.css
  } else {
    casa.addClass("casa-branca");
  }
}

function criaPeca(casas, posicaoAtual){
  var jogo = $("#jogo"); //aqui estamos fazendo a seleção da div do jogo todo, que
                        // incluirá peça + tabuleiro
  var peca = $("<div>"); // criamos a peca como se fosse uma div
  peca.addClass("peca"); // adicionamos a classe peca para ter as caracteristicas de peca do
                        //index.css
  jogo.append(peca); // a div peça será filha da div jogo, caso tenha dúvidas sobre elementos
                      // html criados dinamicamente, basta abrir o console do desenvolvedor no
                      // chrome pra ver todos os elementos html da página (Ctrl + shift + J)
  posicionaPeca(peca, casas, posicaoAtual);

  $( function() {
    peca.draggable(); // precisamos "entrar no mundo do jQuery" com $, pois a função
                      // dragabble só está presente na biblioteca jQueryUI, caso coloquemos
                      // apenas draggable teríamos erro de compilação, já que draggable
                      // não é uma função definida em javascript ou no nosso programa
                      // essa função declara que a peça tem o evento drag e que ele movimenta
                      // a peça pelo DOM
  } );

  return peca;
}

function posicionaPeca(peca, casas, posicaoAtual){
  var idLin = posicaoAtual[0];
  var idCol = posicaoAtual[1];

  var topDif = Math.floor(casas[idLin][idCol].position().top + $("td").height()/2 -
               peca.width()/2); // fazemos a relocação da peça pois inicialmente ela aparecerá
                                // do lado de fora do tabuleiro. o $ do jQuery aqui está
                                // selecionando o primeiro td que encontrar, que já está criado
                                // e vendo sua propriedade de altura
  var leftDif = Math.floor(casas[idLin][idCol].position().left + $("td").width()/2 -
               peca.height()/2);

  peca.css({top:topDif, left: leftDif}); // a função .css serve para alterar dinamicamente os
                                        // atributos css do elemento DOM, no caso peca, mudando
                                        // de fato sua posição na tela
}

function criaPossibilidades(casas, posicaoAtual){
  var peca = $(".peca"); // o . na frente de peça significa que queremos pegar todos os elementos
                        // que possuem a classe peça (só um no nosso caso)

  $(peca).unbind("dragstart"); // aqui estamos o evento de começo de drag
                              // isso acontece porque não queremos que a cada iteração do
                              // gameloop tenhamos um novo evento sendo adicionado ao jogo
                              // pois assim teríamos acumulação, gerando código incosistente,
                              // e logicamente baixa performance (eventos são caros)

  // o one declara que um evento vai ser atribuído uma única vez para aquela peça quando
  // essa função for executada, repare que ainda precisamos do unbind pois se não teríamos
  // vários eventos (mesmo que únicos) atribuídos pro mesmo elemento DOM
  $(peca).one("dragstart", function(){
    var possibs = definePossibilidades(casas, posicaoAtual);

    for (var k = 0; k < possibs.length; k++) {
      var possib = possibs[k];
      casas[possib[0]][possib[1]].addClass("ui-droppable"); // cada casa possível para a jogada
                                                          // terá a borda pintada segundo o css
    }
  })
}

function definePossibilidades(casas, posicaoAtual){
  var possibs = new Array();

  for (var i = 0; i < 2; i++){
    var possib = new Array();

    // só temos duas chances: a peça se movimenta verticalmente para esquerda ou para direita
    if (i == 0){
      possib[0] = posicaoAtual[0] - 1;
      possib[1] = posicaoAtual[1] - 1;
    } else {
      possib[0] = posicaoAtual[0] - 1;
      possib[1] = posicaoAtual[1] + 1;
    }

    if (possib[0] >= 0 && possib[1] >= 0 &&
        possib[0] < casas.length && possib[1] < casas.length){ // tratamento das bordas
      possibs.push(possib);
    }
  }

  return possibs;
}

function movePeca(casas){
  var peca = $(".peca");
  var espacosDisponiveis = $(".ui-droppable");

  jogadaTentada = false;

  for (var i = 0; i < espacosDisponiveis.length; i++) {
    if (!$(espacosDisponiveis[i]).data("droppable")){ // verifica se a casa já não é dropável
                                                      // se ela for, não estamos interessados
                                                      // em adicionar mais um evento à ela à
                                                      // toa, como explicado mais acima
      $(espacosDisponiveis[i]).droppable({ // definimos que os espacos possuem a característica
                                          // droppable do jQueryUI (outra biblioteca do jQuery)

        drop: function(event, ui){ // o evento de drop seguirá a seguinte lógica
          var col = $(this).parent().children().index($(this));
          var row = $(this).parent().parent().children().index($(this).parent());
          // col e row são pegas utilizando funções de parent e children para definir
          // qual é o indíce da coluna que sofreu o evento drop (que é uma td)
          // simplificando: $(this) é a td, .parent() é a tr pai, .children() todas as tds
          // filhas desse pai, .index($(this)) indica o índice do td que foi dropado, assim
          // temos o valor da coluna. O mesmo processamento segue para row
          posicaoAtual = [row, col];
          posicionaPeca(peca, casas, posicaoAtual);
          tentaJogada(true);
        }
      })
    }
  }

  // a peça adquire a classe css "ui-draggable-dragging" do jQueryUI quando ela está sendo
  // "draggada". Logo, quando ela está sendo não está sendo draggada e a jogada não foi
  // dropada em um campo válido, precisamos voltar a peça pra sua antiga posição
  if (!peca.hasClass("ui-draggable-dragging") && !jogadaTentada) {
    posicionaPeca(peca, casas, posicaoAtual);
    tentaJogada(false);
  }
}

function tentaJogada(concluiu){
  var espacosAntigos = $(".ui-droppable");

  for (var i = 0; i < espacosAntigos.length; i++) {
    var espacoAntigo = espacosAntigos[i];

    if (!concluiu){
        $(espacoAntigo).droppable("enable"); // no caso de não ter havido movimento da peça para
                                            // uma nova casa, precisamos habilitar o droppable
                                            // dos espacos que ainda são candidatos
    } else {
        $(espacoAntigo).droppable("disable"); // caso contrário, precisamos de um disable,
                                              // já que se não destruirmos o evento, os espaços
                                              // antigos serão ainda candidatos, o que está
                                              // logicamente errado
    }

    $(espacoAntigo).removeClass("ui-droppable"); // de qualquer forma queremos sumir com a borda
                                                // amarela, para uma nova tentativa
  }

  jogadaTentada = true;
}
