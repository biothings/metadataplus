<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-main fixed-top">
    <router-link class="navbar-brand text-light mainFont" to="/">
      <img alt="metadataplus" src="../assets/img/logosimple.svg" width="30px"/> METADATAPLUS
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

export default {
  name: 'Nav',
  components: {

  }
}
</script>

<style lang="scss">
 @import '../assets//styles/app.module.scss';

</style>
