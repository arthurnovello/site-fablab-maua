$(document).ready(function () {
    $('#agendamento').change(function() {
        if (($('#solicitante').val() == 333333 || $('#solicitante').val() == 3)) {
            $('.aluno-div').fadeIn('fast');
        } else {
            $('.aluno-div').fadeOut('fast');
        }
        if ($('#outro').val() == 4) {
            $('#outroInput').removeClass('hide');
        } else {
            $('#outroInput').addClass('hide');
        }
        if ($('#agendamento-radio').val() == 1) {
            $('#agendamento-div').fadeIn('fast');
        } else {
            $('#agendamento-div').fadeOut('fast');
        }
        if ($('#fabricacao-radio').is(':checked')) {
            $('#fabricacao-div').removeClass('hide');
        } else {
            $('#fabricacao-div').addClass('hide');
        }
    });

    sendHttpRequest('GET', 'http://localhost:5000/Curso/').then(res => {
      res.Cursos.forEach(option => {
        var opt = document.createElement('option');
        opt.innerText = option.curso;
        opt.value = option.id
        document.getElementById('curso').append(opt);
      });
    });

    sendHttpRequest('GET', 'http://localhost:5000/Sala/').then(res => {
      res.Salas.forEach(option => {
        var opt = document.createElement('option');
        opt.innerText = option.sala;
        opt.value = option.id
        document.getElementById('sala').append(opt);
      });
    });

    sendHttpRequest('GET', 'http://localhost:5000/Solicitante/').then(res => {
      res.Solicitantes.forEach(option => {
        var opt = document.createElement('option');
        opt.innerText = option.solicitante;
        opt.value = option.id
        document.getElementById('solicitante').append(opt);
      });
    });

    sendHttpRequest('GET', 'http://localhost:5000/Solicitacao/').then(res => {
      res.Solicitacoes.forEach(option => {
        var opt = document.createElement('option');
        opt.innerText = option.solicitacao;
        opt.value = option.id
        document.getElementById('solicitacao').append(opt);
      });
    });

    $("#btnEnviar").click(function(evt){
      evt.preventDefault();
      var result = $("#agendamento").serializeArray().reduce((acc, cur) => {
        return {
          ...acc,
          [cur.name]: cur.value
        }
      }, {});

      sendHttpRequest('POST', 'http://localhost:5000/Pedido/', result)
        .then(function(response){
          console.log(response);
          alert(response.message)
        })
        .catch((err) => {console.log(err, err.data); alert(err.data)});
    });

    $("#btnConsultar").click(function(evt){
      evt.preventDefault();
      $("#filtroPedidos").html("");
      var result = $("#consultaPedido").serializeArray().reduce((acc, cur) => {
        return {
          ...acc,
          [cur.name]: cur.value
        }
      }, {});

      // sendHttpRequest('POST', 'http://localhost:5000/Pedido/', result).then((res => {
      //   console.log(res)
      //   res.Status.forEach(option => {
      //   console.log(option)
      //   // var opt = document.createElement('input');
      //   if(option.concluido == false){
      //     document.getElementById('filtroPedidos').innerText = ("Ultimo pedido ainda não foi concluído");
      //   }
      //   else{
      //     document.getElementById('filtroPedidos').innerText = ("Pedido concluído");
      //   }
      //   // opt.value = option.concluido
      //   // document.getElementById('filtroPedidos').append(opt);
      //   });
      //   }));
      // });

      sendHttpRequest('POST', 'http://localhost:5000/Pedido/', result).then((res => {
        console.log(res)
        res.Status.forEach(option => {
        console.log(option)
        var ul = document.createElement('ul');
        var liIDPedido = document.createElement('li');
        var liAprovado = document.createElement('li');
        var liMassa = document.createElement('li');
        var liTempo = document.createElement('li');
        var liConcluido = document.createElement('li');
        var liTermino = document.createElement('li');
        liIDPedido.innerHTML = "ID do pedido: " + option.id_pedido;
        liAprovado.innerHTML = "Aprovado: " + res.Pedidos[0].aprovado;
        liMassa.innerHTML = "Massa: " + option.massa;
        liTempo.innerHTML = "Tempo: " + option.tempo;
        liConcluido.innerHTML = "Concluído: " + option.concluido;
        liTermino.innerHTML = "Término: " + option.termino;
        // console.log(option.termino);
        
        
        // var liMassa = document.createElement('li').innerHTML(String(option.massa));
        // var liTempo = document.createElement('li').innerHTML(String(option.tempo));
        // var liConcluido = document.createElement('li').innerHTML(String(option.concluido));
        // var liTermino = document.createElement('li').innerHTML(String(option.termino));
        // opt.value = option.concluido/termino/tempo/massa
       
        ul.appendChild(liIDPedido);
        ul.appendChild(liAprovado)
        ul.appendChild(liMassa);
        ul.appendChild(liTempo);
        ul.appendChild(liConcluido);
        ul.appendChild(liTermino);
        document.getElementById('filtroPedidos').append(ul);
        });
        }));
      });



    $("#inputEmail").focusout(function(evt){
      sendHttpRequest('POST', 'http://localhost:5000/Pessoa/',{"email":$("#inputEmail").val()}).then(res => {
        res.Pessoa.forEach(option => {
          $("#inputNome").val(option.nome);
          $("#inputEmail").val(option.email);
          $("#inputRa").val(option.ra);
        });
      });
    });

});

const sendHttpRequest = (method, url, data) => {
  console.log(data)
  return fetch(url, {
    method: method,
    body: JSON.stringify(data),
    headers: data ? { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' } : {}
  }).then(response => {
    if (response.status >= 400) {
      return response.json().then(errResData => {
        const error = new Error('Something went wrong requesting your data');
        error.data = errResData;
        throw error;
      });
    }

    return response.json();
  });
}
