<template>
  <div>
    <div class="container-fluid hero bg-main text-center d-flex justify-content-center align-items-center">
      <div>
        <img alt="metadataplus" src="../assets/img/logofull.svg" class="w-100"/>
        <br />
        <h3 class="text-light font-weight-light">Schema.org-Standard Structured Metadata Injector</h3>
      </div>
    </div>
    <div class="bg-sec jumbotron m-0">
      <div class="container row m-auto">
        <div class="col-sm-12 col-md-4 d-flex justify-content-center align-items-center">
          <div class="text-center">
            <img src="../assets/img/why.svg" alt="why use schema.org" class="w-50 d-block m-auto"/>
            <h1 class="text-light">WHY SCHEMA.ORG<span class="text-main">?</span></h1>
          </div>
        </div>
        <div class="col-sm-12 col-md-8 d-flex justify-content-center align-items-center">
          <div data-aos="zoom-out">
            <p>
              Currently, there are many standards and schemas for marking up different types of information on web pages. As a result, it is difficult for webmasters to decide on the most relevant and supported markup standards to use.
            </p>
            <p>
              <a href="https://discovery.biothings.io/schema-playground" target="_blank">Creating a schema</a> supported by all the major search engines makes it easier for webmasters to add markup, which makes it easier for search engines to create rich search features for users.
            </p>
            <p>
              Learn more about <a href="https://schema.org/" target="_blank" rel="noreferrer">Schema.org</a>.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-main-color jumbotron m-0">
      <div class="container row m-auto">
        <div class="col-sm-12 col-md-8  d-flex justify-content-center align-items-center">
          <div data-aos="zoom-out">
            <p>
              Metadata and data should be easy to find for both humans and computers. Machine-readable metadata are essential for automatic discovery of datasets and services.
            </p>
            <p>
              Following a widely accepted standard ensures your data will be easy for machines to find and understand.
            </p>
          </div>
        </div>
        <div class="col-sm-12 col-md-4 d-flex justify-content-center align-items-center">
          <div class="text-center">
            <img src="../assets/img/disc.svg" alt="discovery" class="w-50 d-block m-auto"/>
            <h1 class="text-light">FINDABLE METADATA<span class="text-main">?</span></h1>
          </div>
        </div>
      </div>
    </div>
    <div class="bg-sec jumbotron m-0">
      <div class="container row m-auto">
        <div class="col-sm-12 col-md-4 d-flex justify-content-center align-items-center">
          <h1 class="text-light">MOTIVATION</h1>
        </div>
        <div class="col-sm-12 col-md-8 d-flex justify-content-center align-items-center">
          <div data-aos="zoom-out">
            <p>
              Following a standard for structured metadata can impact the discovery of your dataset and will help our efforts to make data <a href="https://www.go-fair.org/fair-principles/" rel="noreferrer" target="_blank">FAIR</a> (Findable, Accessible, Interoperable and Reusable).
            </p>
            <p>
              Interoperable data makes more powerful networks of knowledge that the research community can use to advance research findings faster in today's fast-growing tech world.
            </p>
          </div>
        </div>
      </div>
    </div>
    <div class="jumbotron card card-image m-0" style="background-image: url(https://media2.giphy.com/media/5vidmSHUsyoybSYNN0/giphy.gif?cid=790b76111ca0090d26f425bde6806c7d76146718da58ed2e&rid=giphy.gif);background-size:cover;">
      <div class="text-white text-center py-5 px-4">
        <div class="container">
          <h1 class="card-title h1-responsive pt-3 mb-5 font-bold"><strong>SEE IT IN ACTION</strong></h1>
          <p class="mx-5">
            Some dataset web sources out there offer dataset information that is not optimized for machines to be able to find and understand.
          </p>
          <p>
            We fix this by reading the content of those webpages and reformat published dataset metadata to schema.org standard.
          </p>
          <p>
            Some sources include:
          </p>
          <div class="d-flex justify-content-center">
            <div class="bg-main w-25 p-2 rounded">
              <img src="../assets/img/geo_main.gif" alt="GEO" width="100px" class="bg-light m-1"/>
              <a class="btn btn-outline-light" rel="noreferrer" href="https://discovery.biothings.io:8088/_random.html?redirect" target="_blank">
                <i class="fas fa-clone left"></i> See An Example
              </a>
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
