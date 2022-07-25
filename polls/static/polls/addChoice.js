document.addEventListener("DOMContentLoaded", function() {
  console.log('LOGGING!');
  let addChoiceBtn = document.getElementById('newChoice');
  addChoiceBtn.addEventListener('click', function(e) {
    console.log('add btn clicked!');
    e.preventDefault();
    let i = document.querySelectorAll('.choiceField').length;
    console.log(i);
    let newInput = document.createElement('input');
    newInput.setAttribute('type', 'text');
    newInput.setAttribute('id', `choiceField-${i}`);
    newInput.setAttribute('name', `choiceField-${i}`);
    document.getElementById('choices').appendChild(newInput);
  });
});