$(document).ready(function(){

  const heightWelcome = $('.bg-welcome').height();

  const parallax1 = rallax('.parallax1')
  parallax1.when(
    () => window.scrollY > heightWelcome - heightWelcome/4.5,
    () => parallax1.changeSpeed(0.3)
  ).when(
    () => window.scrollY < heightWelcome - heightWelcome/4.5,
    () => parallax1.changeSpeed(0)
  ).when(
    () => window.scrollY > heightWelcome + 100,
    () => parallax1.changeSpeed(0)
  );

  const parallax2 = rallax('.parallax2')
  parallax2.when(
    () => window.scrollY > heightWelcome - heightWelcome/4.5,
    () => parallax2.changeSpeed(0.4)
  ).when(
    () => window.scrollY < heightWelcome - heightWelcome/4.5,
    () => parallax2.changeSpeed(0)
  ).when(
    () => window.scrollY > heightWelcome + 100,
    () => parallax2.changeSpeed(0)
  );

  const parallax3 = rallax('.parallax3')
  parallax3.when(
    () => window.scrollY > heightWelcome - heightWelcome/4.5,
    () => parallax3.changeSpeed(0.5)
  ).when(
    () => window.scrollY < heightWelcome - heightWelcome/4.5,
    () => parallax3.changeSpeed(0)
  ).when(
    () => window.scrollY > heightWelcome + 100,
    () => parallax3.changeSpeed(0)
  );
  

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

  lax.setup() // init

  const updateLax = () => {
    lax.update(window.scrollY+50)
    window.requestAnimationFrame(updateLax)
  }

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
            scrollTop: $(".second").offset().top-72},
            'slow');
    });
    
});