$(document).ready(function () {
    $('#agendamento').change(function() {
        if (($('#aluno').is(':checked')) || ($('#exAluno').is(':checked'))) {
            $('.aluno-div').fadeIn('fast');
        } else {
            $('.aluno-div').fadeOut('fast');
        }
        if ($('#outro').is(':checked')) {
            $('#outroInput').removeClass('hide');
        } else {
            $('#outroInput').addClass('hide');
        }
        if ($('#agendamento-radio').is(':checked')) {
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
    // Add the following code if you want the name of the file appear on select
    $(".custom-file-input").on("change", function() {
        var fileName = $(this).val().split("\\").pop();
        $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
    });

    const sendHttpRequest = (method, url, data) => {
        return fetch(url, {
          method: method,
          body: JSON.stringify(data),
          headers: data ? { 'Content-Type': 'application/json' } : {}
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
});
