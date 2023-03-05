/**
* Template Name: Siimple - v4.9.0
* Template URL: https://bootstrapmade.com/free-bootstrap-landing-page/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
function limparQrcode() {
    document.getElementById("qrcode").innerHTML = "";
    }

const gerarQrcodeBtn = document.getElementById("gerar-qrcode");
const emailInput = document.getElementById("epix");

gerarQrcodeBtn.addEventListener("click", function(event) {
  if (emailInput.value === "") {
    event.preventDefault();
    alert("Por favor, informe seu e-mail.");
  }
});
//------------------------------------------------------------------------------------
// Essa funcao esconde e mostra todos os formularios
 function mostrarFormulario(formularioId) {
        // Esconde todos os formulários
        document.querySelectorAll('form[id$="-form"]').forEach(formulario => {
            formulario.style.display = 'none';
        });

        // Mostra o formulário correto
        document.getElementById(formularioId).style.display = 'block';
    }




(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Mobile nav toggle
   */
  const toogleNav = function() {
    let navButton = select('.nav-toggle')
    navButton.classList.toggle('nav-toggle-active')
    navButton.querySelector('i').classList.toggle('bx-x')
    navButton.querySelector('i').classList.toggle('bx-menu')

    select('.nav-menu').classList.toggle('nav-menu-active')
  }
  on('click', '.nav-toggle', function(e) {
    toogleNav();
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.nav-menu .drop-down > a', function(e) {
    e.preventDefault()
    this.nextElementSibling.classList.toggle('drop-down-active')
    this.parentElement.classList.toggle('active')
  }, true)

  /**
   * Scrool links with a class name .scrollto
   */
  on('click', '.scrollto', function(e) {
    if (select(this.hash)) {
      select('.nav-menu .active').classList.remove('active')
      this.parentElement.classList.toggle('active')
      toogleNav();
    }
  }, true)

})()