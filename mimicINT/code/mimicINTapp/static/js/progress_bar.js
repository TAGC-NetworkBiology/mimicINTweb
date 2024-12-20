function formatTime(seconds) {
  // Convertir le nombre de secondes en heures, minutes et secondes
  var hours = Math.floor(seconds / 3600);
  var minutes = Math.floor((seconds % 3600) / 60);
  var seconds = Math.floor(seconds % 60);
  // Formater le temps sous la forme HH:MM:SS
  return ('0' + hours).slice(-2) + ':' + ('0' + minutes).slice(-2) + ':' + ('0' + seconds).slice(-2);
  }

function updateProgressBar(){
    var now = new Date();
    var submissionDate = new Date('{{ Job_infos.submission_date }}');
    var elapsedTime = (now.getTime() - submissionDate.getTime()) / 1000;
    totalDuration = {{ sum_rule_duration }};
    var progress = Math.round(100 * elapsedTime / totalDuration);

    $('.progress-bar').attr('aria-valuenow', progress).css('width', progress + '%');

}

setInterval(updateProgressBar, 1000);