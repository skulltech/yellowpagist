// custom javascript

$( document ).ready(() => {
  console.log('Sanity Check!');
});

$('#submitBtn').on('click', function() {
  $.ajax({
    url: '/enqueue',
    data: $(this).data('type'),
    method: 'POST'
  })
  .done((res) => {
    getStatus(res.data.task_id)
  })
  .fail((err) => {
    console.log(err)
  })
})

function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = 
    $("#loadingGIF").show();
    $("#submitBtn").hide();
    const taskStatus = res.data.task_status;

    if (taskStatus === 'finished' || taskStatus === 'failed') {
      window.location.assign(`/download/${taskID}`);
      return false;
    }
    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 1000);
  })
  .fail((err) => {
    console.log(err)
  })
}
