import React from "react";
import Carousel from "react-bootstrap/Carousel";
import "bootstrap/dist/css/bootstrap.min.css";
import "../Carousel.css";

function AboutUs() {
  return (
    <Carousel fade>
      <Carousel.Item>
        <img
          className="d-block w-100"
          src={
             "https://i.ibb.co/wBqFjMH/fresh-gourmet-meal-wooden-table-close-up-generative-ai.jpg"
          }
          alt="First slide"
        />
        <Carousel.Caption>
          <h3>Byenvini nan Woody Vert - Restaurant</h3>
          <p>
            Vin dekouvri yon eksperyans gou inik nan Restoran nou an. Nou ofri yon meni ki plen bon gou, 
            ki enspire pa kwizin Ayisyen otantik, prepare ak engredyan fre de bon kalite.
          </p>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img
          className="d-block w-100"
          src={
            "https://i.ibb.co/ggvh0WR/fresh-vegetable-pasta-meal-gourmet-crockery-plate-generative-ai.jpg"
          }
          alt="Second slide"
        />
        <Carousel.Caption>
          <h3>Toujou panse vin jwenn nou</h3>
          <p>
           Kenbe tout manje ou renmen nan yon sèl plas ki fasil pou jwenn, 
           pandan w ap mete yon ti sèl nan pwofil ou pou adapte l ak bezwen ou.
          </p>
        </Carousel.Caption>
      </Carousel.Item>
      <Carousel.Item>
        <img
          className="d-block w-100"
          src={
            "https://i.ibb.co/Fnc5dyx/freshly-grilled-meat-wooden-plate-generated-by-ai.jpg"
          }
          alt="Third slide"
        />
        <Carousel.Caption>
          <h3>Note chak plaw yo</h3>
          <p>
           Sonje bon gou ki genyen nan chak pla kew dekouvri nan Woody Vert.
           Nou vle pote pi bon gou lakay ou. 
          </p>
        </Carousel.Caption>
      </Carousel.Item>
    </Carousel>
  );
}

export default AboutUs;
