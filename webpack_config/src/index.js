import anime from 'animejs';

anime({
    targets: '.circle-1',
    keyframes: [
        {translateY: -400},
        {translateX: 750},
        {translateY: 400},
        {translateX: 0},
        {translateY: 0}
    ],
    duration: 10000,
    easing: 'easeOutElastic(1, .8)',
    loop: true
})

anime({
    targets: '.circle-2',
    keyframes: [
      {translateY: -40},
      {translateX: 250},
      {translateY: 40},
      {translateX: 0},
      {translateY: 0}
    ],
    duration: 4000,
    easing: 'easeOutElastic(1, .8)',
    loop: true
  });