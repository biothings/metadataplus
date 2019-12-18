<template>
<footer class="page-footer font-small blue pt-4 bg-dark text-light p-5">
  <div class="container-fluid text-center text-md-left">
    <div class="row">
      <div class="col-md-6 mt-md-0 mt-3">
        <h5 class="mainFont text-main"><strong>METADATA <span class="text-sec">PLUS</span></strong></h5>
        <p class="text-muted text-uppercase">Schema.org-Standard Structured Metadata Injector</p>
      </div>
      <hr class="clearfix w-100 d-md-none pb-3">
      <div class="col-md-3 mb-md-0 mb-3">
        <h5 class="text-uppercase">Links</h5>
        <ul class="list-unstyled">
          <li>
            <a href="#!">BioThings</a>
          </li>

        </ul>
      </div>
      <div class="col-md-3 mb-md-0 mb-3">
        <h5 class="text-uppercase">Data Discovery Engine</h5>
        <ul class="list-unstyled">
          <li>
            <a href="https://discovery.biothings.io/schema-playground" target="_blank">Create a shema</a>
          </li>
          <li>
            <a href="https://discovery.biothings.io/best-practices" target="_blank">Metadata discovery</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer-copyright text-center py-3">© 2019 Copyright:
    <a href="https://biothings.io"> BioThings.io</a>
  </div>

</footer>
</template>

<script>

export default {
  name: 'Footer',
  components: {

  }
}
</script>

<style lang="scss">
 @import '../assets//styles/app.module.scss';

</style>
