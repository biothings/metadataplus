<template>
  <div id="app">
    <Nav/>
    <transition name="fade">
      <router-view></router-view>
    </transition>
    <Footer/>
  </div>
</template>

<script>
import Nav from "./components/Nav"
import Footer from "./components/Footer"
export default {

  name: 'app',
  components: {
    Nav,Footer
  }
}
</script>

<style lang="scss">
 @import './assets//styles/app.module.scss';
 .hero{
   background-image: url('~@/assets/img/back.jpg');
   background-position: center;
   background-size: cover;
   position: relative;
   min-height: 100vh;
   overflow: hidden;
 }
 .bg-about{
   background-image: url("~@/assets/img/back2.svg");
   background-repeat: no-repeat;
  background-position: center center;
  background-size: contain;
 }
 .bg-logo{
   background-image: url("~@/assets/img/background.svg");
   background-repeat: no-repeat;
  background-position: left;
  background-size: cover;
 }
 .btn-main{
   background-image: url("~@/assets/img/btnmain.svg");
   background-repeat: no-repeat;
  background-position: left;
  background-size: cover;
  // background-color: #7A7ADC;
 }
 .btn-sec{
   background-image: url("~@/assets/img/btnsec.svg");
   background-repeat: no-repeat;
  background-position: left;
  background-size: cover;
  // background-color: #FF616D;
 }

</style>
