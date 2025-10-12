import React from "react";
import { CDBBtn, CDBIcon, CDBBox } from "cdbreact";
import "../index.css";
export const Footer = () => {
  return (
    <div id="footer">
      <CDBBox
        display="flex"
        justifyContent="between"
        alignItems="center"
        className="mx-auto py-4 flex-wrap"
        style={{ width: "80%" }}>
        <CDBBox display="flex" alignItems="center">
          <a href="/" className="d-flex align-items-center p-0 text-dark">
            <span className="ms-4 h2 mb-0 font-weight-bold-">
              Woody Vert - Restaurant
            </span>
          </a>
          <small className="ms-2">
            &copy; Woody BELONY, 2025. All rights reserved.
          </small>
        </CDBBox>
        <CDBBox display="flex">
          <a
            href="https://www.instagram.com/woobeegraphic/"
            target="_blank"
            rel="noopener noreferrer">
            <CDBBtn flat color="dark" className="p-2">
              <CDBIcon fab icon="instagram" />
            </CDBBtn>
          </a>
          <a
            href="https://www.linkedin.com/in/woodybelony/"
            target="_blank"
            rel="noopener noreferrer">
            <CDBBtn flat color="dark" className="mx-3 p-2" src="">
              <CDBIcon fab icon="linkedin" />
            </CDBBtn>
          </a>
          <a
            href="https://github.com/BeloWeb"
            target="_blank"
            rel="noopener noreferrer">
            <CDBBtn flat color="dark" className="p-2">
              <CDBIcon fab icon="github" />
            </CDBBtn>
          </a>
        </CDBBox>
      </CDBBox>
    </div>
  );
};

export default Footer;
