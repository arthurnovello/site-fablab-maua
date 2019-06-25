$(document).ready(function(){

  var scrollTop = 0;
  $(window).scroll(function(){
    scrollTop = $(window).scrollTop();
      $('.counter').html(scrollTop);
    
    if (scrollTop >= 80) {
      $('.navbar').addClass('scrolled-navbar');
    } else if (scrollTop < 100) {
      $('.navbar').removeClass('scrolled-navbar');
    } 
    
  });

  particlesJS("particles-js", {
      particles: {
          number: { value: 20, density: { enable: true, value_area: 400 } },
          color: { value: "#ffffff" },
          shape: {
          type: "circle",
          stroke: { width: 0, color: "#000000" },
          polygon: { nb_sides: 3 },
          image: { src: "img/github.svg", width: 100, height: 100 }
          },
          opacity: {
          value: 0.7,
          random: true,
          anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false }
          },
          size: {
          value: 1.5,
          random: true,
          anim: { enable: false, speed: 40, size_min: 0.1, sync: false }
          },
          line_linked: {
          enable: false,
          distance: 1170.4908044318315,
          color: "#f7f7f7",
          opacity: 0.4,
          width: 1
          },
          move: {
          enable: true,
          speed: 1.8,
          direction: "none",
          random: false,
          straight: false,
          out_mode: "out",
          bounce: false,
          attract: { enable: false, rotateX: 600, rotateY: 1200 }
          }
      },
      interactivity: {
          detect_on: "canvas",
          events: {
          onhover: { enable: false, mode: "grab" },
          onclick: { enable: false, mode: "push" },
          resize: true
          },
          modes: {
          grab: { distance: 400, line_linked: { opacity: 1 } },
          bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
          repulse: { distance: 200, duration: 0.4 },
          push: { particles_nb: 4 },
          remove: { particles_nb: 2 }
          }
      },
      retina_detect: true
  });

  lax.setup({
    breakpoints: { small: 0, large: 992 }
  }) // init

  var updateLax = function() {
    lax.update(window.scrollY+50)
    window.requestAnimationFrame(updateLax)
  };

  window.addEventListener("resize", function() {
    lax.updateElements()
  });

  window.requestAnimationFrame(updateLax)

    $(".scroll").click(function(e) {

      e.preventDefault();
      var position;
      $(this).hasClass('contato') ? position = $(document).height() : position = ($($(this).attr("href")).offset().top)-95;
      $("body, html").animate({
        scrollTop: position
      } /* speed */ );
    });

    $(".scroll-downs").click(function() {
        $('html,body').animate({
            scrollTop: $(".sobre-scroll").offset().top-72},
            1000);
    });

    $(".sobre").click(function() {
      $('html,body').animate({
          scrollTop: $(".sobre-scroll").offset().top-72},
          1000);
    });

    $(".home").click(function() {
      $('html,body').animate({
          scrollTop: $('body').offset().top-72},
          1000);
    });

    $(".projetos").click(function() {
      $('html,body').animate({
          scrollTop: $(".projetos-scroll").offset().top-72},
          1000);
    });

    $(".maquinas").click(function() {
      $('html,body').animate({
          scrollTop: $(".maquinas-scroll").offset().top-72},
          1000);
    });

    $(".agendamento").click(function() {
      $('html,body').animate({
          scrollTop: $(".agendamento-scroll").offset().top-72},
          1000);
    });
    
});