<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-main fixed-top">
    <router-link class="navbar-brand text-light mainFont" to="/" id="header">
      <img alt="metadataplus" src="../assets/img/logosimple.svg" width="30px"/> METADATA <span class="text-sec">PLUS</span>
    </router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" to="/about">ABOUT</router-link>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    document.getElementById("header").style.fontSize = "1em";
  } else {
    document.getElementById("header").style.fontSize = "2em";
  }
}

export default {
  name: 'Nav',
  components: {

  }
}
</script>

<style lang="scss">
 @import '../assets//styles/app.module.scss';
</style>
