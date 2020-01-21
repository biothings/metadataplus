<template>
  <div>
    <div class="container-fluid hero bg-main text-center d-flex justify-content-center align-items-center">
      <div>
        <img alt="metadataplus" src="../assets/img/logofull.svg" class="w-100"/>
        <br />
        <h3 class="text-light font-weight-light"><a class="text-light" href="https://schema.org/" target="_blank" rel="noreferrer">Schema.org</a>-Standard Structured Metadata Injector</h3>
        <p class="mt-4 justify-content-center d-flex">
          <router-link class="btn btn-outline-light btn-main m-3" to="/about">Learn How It Works</router-link>
          <a class="btn btn-outline-light m-3 btn-sec" rel="noreferrer" href="http://metadataplus.biothings.io/geo/GSE9878" target="_blank">
            <i class="fas fa-clone left"></i> See An Example
          </a>
        </p>
      </div>
    </div>
    <div class="bg-main-color jumbotron m-0">
      <div class="container row m-auto">
        <div class="col-sm-12 col-md-8  d-flex justify-content-center align-items-center">
          <div>
            <p>
              Some data sources publish valuable dataset information on a format only readable by humans. If machines can't systematically find and understand this information, valuable contributions could be missed by related research efforts.
            </p>
            <p>
              Metadata and data should be easy to find for both humans and computers.
            </p>
          </div>
        </div>
        <div class="col-sm-12 col-md-4 d-flex justify-content-center align-items-center">
          <div class="text-center">
            <img src="../assets/img/why.svg" alt="discovery" class="w-50 d-block m-auto"/>
            <h1 class="text-light">THE PROBLEM<span class="text-main">!</span></h1>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-sec jumbotron m-0">
      <div class="container row m-auto">
        <div class="col-sm-12 col-md-4 d-flex justify-content-center align-items-center">
          <div class="text-center">
            <img src="../assets/img/disc.svg" alt="why use schema.org" class="w-50 d-block m-auto"/>
            <h1 class="text-light">WHY SCHEMA.ORG<span class="text-main">?</span></h1>
          </div>
        </div>
        <div class="col-sm-12 col-md-8 d-flex justify-content-center align-items-center">
          <div>
            <p>
              Currently, there are many standards and schemas for marking up different types of information on web pages. As a result, it is difficult for webmasters to decide on the most relevant and supported markup standards to use.
            </p>
            <p>
              <a class="text-light" href="https://schema.org/" target="_blank" rel="noreferrer">Schema.org</a> provides a widely accepted format regonizable by major search engines and data portals.
            </p>
            <p>
              <a class="text-light" href="https://discovery.biothings.io/schema-playground" target="_blank">Creating a schema</a> supported by all the major search engines makes it easier for webmasters to add markup, which makes it easier for search engines to create rich search features for users.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-main-color jumbotron m-0">
      <div class="container row m-auto">
        <div class="col-sm-12 col-md-8 d-flex justify-content-center align-items-center">
          <div>
            <p>
              Following a standard and reusable data model for structured metadata can impact the discovery of your dataset and will help our efforts to make data <a class="text-light" href="https://www.go-fair.org/fair-principles/" rel="noreferrer" target="_blank">FAIR</a> (Findable, Accessible, Interoperable and Reusable).
            </p>
            <p>
              Interoperable data makes more powerful networks of knowledge that the research community can benefit from to advance research findings faster in today's fast-growing tech world.
            </p>
          </div>
        </div>
        <div class="col-sm-12 col-md-4 d-flex justify-content-center align-items-center">
          <div class="text-center">
            <img src="../assets/img/motivation.svg" alt="motivation" class="w-75 d-block m-auto"/>
            <h1 class="text-light">MOTIVATION</h1>
          </div>
        </div>
      </div>
    </div>
    <div class="jumbotron card card-image m-0 bg-main bg-logo ">
      <div class="text-white text-center py-5 px-4">
        <div class="container p-2" style="background:rgba(0,0,0,.2)">
          <div class="pt-5 pb-5" data-aos="fade-up">
            <h1 class="card-title h1-responsive pt-3 mb-5 font-bold mainFont"><strong>METADATA <span class="text-sec">PLUS</span></strong></h1>
            <p class="mx-5">
              Some dataset web sources out there offer dataset information that is not optimized for machines to be able to find and understand.
            </p>
            <p>
              We fix this by reading the content of those webpages and reformat published dataset metadata to schema.org standard.
            </p>
            <p>
              The result is metadata that can be harvested by data portals and understood by search engines.
            </p>
            <h3><router-link class="nav-link" to="/about">Learn About How It Works</router-link></h3>
            <h4>or</h4>
            <h3 class="card-title h1-responsive pt-3 mb-5 text-sec"><strong>See It In Action:</strong></h3>
            <div class="d-flex justify-content-center">
              <div class="bg-main w-50 p-2 rounded">
                <img src="../assets/img/geo_main.gif" alt="GEO" width="100px" class="bg-light m-1"/>
                <a class="btn btn-outline-light" rel="noreferrer" href="/geo/_random.html" target="_blank">
                  <i class="fas fa-clone left"></i> See An Example
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AOS from 'aos';
import 'aos/dist/aos.css'; // You can also use <link> for styles
// ..
AOS.init();

export default {
  name: 'home',
  components: {
  }
}
</script>
