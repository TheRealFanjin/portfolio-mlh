const submitForm = document.getElementById('post-form');

submitForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(submitForm);
  await fetch('https://fanjin.dev/api/timeline_post', {
      method: 'POST',
      body: formData
  }).then(response => {
      if (response.ok){
          window.location.reload();
      }else {
          alert('Error: ' + response.message);
      }
      return response.json();
  }).catch(error => {
      console.log(error);
  })
})