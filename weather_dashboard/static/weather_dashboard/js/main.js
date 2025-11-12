document.addEventListener('DOMContentLoaded', function () {
  // Entry animations
  document.querySelectorAll('.animate-up').forEach(function (el, i) {
    el.style.animationDelay = (i * 80) + 'ms';
    el.classList.add('animated-up');
  });
  document.querySelectorAll('.animate-fade').forEach(function (el, i) {
    el.style.animationDelay = (i * 100) + 'ms';
    el.classList.add('animated-fade');
  });

  // Recent search clicks
  document.querySelectorAll('.recent-item').forEach(function (li) {
    li.addEventListener('click', function () {
      var city = this.getAttribute('data-city');
      var input = document.querySelector('#id_city');
      if (input) {
        input.value = city;
        // small pulse to indicate
        input.classList.add('pulse');
        setTimeout(function () { input.classList.remove('pulse'); }, 600);
        // submit form
        var form = document.querySelector('#city-form');
        if (form) { form.submit(); }
      }
    });
  });

  // Form submit -> show spinner overlay
  var form = document.querySelector('#city-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      var overlay = document.getElementById('spinner-overlay');
      if (overlay) {
        overlay.style.display = 'flex';
        overlay.setAttribute('aria-hidden', 'false');
      }
      // allow form to submit normally
    });
  }

  // Subtle background animation based on condition
  var condition = document.body.getAttribute('data-condition');
  if (condition) {
    document.body.classList.add('cond-' + condition.replace(/\s+/g,'-'));
  }
});
