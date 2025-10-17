// django/assets/js/login_intro.js

import { gsap } from "gsap";

const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

// Aparece la cuadrícula del fondo
tl.to(".intro-grid", { opacity: 1, duration: 1 })
  // Aparece el logo
  .to(".intro-logo", { opacity: 1, y: 0, scale: 1, duration: 1.2 }, "-=0.5")
  // Pulso principal (crece, destella y se retrae suavemente)
  .to(
    ".intro-pulse",
    {
      opacity: 1,
      scale: 3,
      duration: 0.9,
      boxShadow: "0 0 25px 8px rgba(0,255,255,0.6)",
      onComplete: () => {
        gsap.to(".intro-pulse", {
          scale: 0.8,
          opacity: 0.6,
          duration: 0.5,
          ease: "power2.inOut",
          onComplete: () => {
            gsap.to(".intro-pulse", {
              scale: 4.2,
              opacity: 0,
              duration: 0.8,
              ease: "power1.in",
            });
          },
        });
      },
    },
    "-=0.8"
  )
  // Brillo del fondo al final
  .to(".intro-bg", { filter: "brightness(0.9) blur(0px)", scale: 1, duration: 1.2 })
  // Desvanece el intro y muestra el login
  .to("#intro", {
    opacity: 0,
    duration: 0.2,
    onComplete: () => {
      document.getElementById("intro").style.display = "none";
      document.getElementById("login-content").style.opacity = 1;
    },
  });
