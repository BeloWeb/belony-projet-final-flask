import React from "react";
import { Formik, Form, Field, useField, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useSnackbar } from "notistack";
import "../AddRestaurant.css";

const formFields = [
  { name: "name", label: "Name", type: "text" },
  { name: "rating", label: "Rating", type: "number", min: "1", max: "5" },
  { name: "image_url", label: "Image URL", type: "text" },
  { name: "phone_number", label: "Phone Number", type: "tel", pattern: "\\d*" },
  { name: "address", label: "Address", type: "text" },
];

const RatingInput = ({ min, max, ...props }) => {
  const [field, , helpers] = useField(props);
  return (
    <input
      {...field}
      {...props}
      type="number"
      min={min}
      max={max}
      onChange={(e) => {
        const value = Math.max(min, Math.min(max, Number(e.target.value)));
        helpers.setValue(value);
      }}
    />
  );
};

const PhoneInput = ({ ...props }) => {
  const [field, , helpers] = useField(props);
  return (
    <input
      {...field}
      {...props}
      type="tel"
      onChange={(e) => {
        const value = e.target.value.replace(/\D/g, "");
        helpers.setValue(value);
      }}
    />
  );
};

const initialValues = formFields.reduce((values, field) => {
  values[field.name] = "";
  return values;
}, {});

const validationSchema = Yup.object({
  name: Yup.string().required("Name is required"),
  rating: Yup.number()
    .min(1, "Rating must be 1 or higher")
    .max(5, "Rating must be 5 or lower")
    .required("Rating is required"),
  image_url: Yup.string().url("Invalid URL").required("Image URL is required"),
  phone_number: Yup.string()
    .matches(/^\d+$/, "Phone number must be numeric")
    .required("Phone number is required"),
  address: Yup.string().required("Address is required"),
});

const AddRestaurantForm = () => {
  const { enqueueSnackbar } = useSnackbar();

  const handleSubmit = async (values, { setSubmitting, resetForm }) => {
    try {
      const response = await fetch("/restaurants", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      if (response.ok) {
        enqueueSnackbar("Restaurant added successfully", {
          variant: "success",
        });
        resetForm();
      } else {
        enqueueSnackbar("Failed to add restaurant", { variant: "error" });
      }
    } catch (error) {
      enqueueSnackbar("Error submitting form", { variant: "error" });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-page-container">
      <div className="form-container">
        <img src="./addrest.jpg" alt="Right Side" />
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}>
          {({ isSubmitting }) => (
            <Form className="add-restaurant-form">
              {formFields.map((field) => {
                let Component =
                  field.type === "number"
                    ? RatingInput
                    : field.type === "tel"
                    ? PhoneInput
                    : "input";
                return (
                  <div key={field.name}>
                    <label htmlFor={field.name}>{field.label}:</label>
                    <Field as={Component} {...field} />
                    <ErrorMessage
                      name={field.name}
                      component="div"
                      className="error-message"
                    />
                  </div>
                );
              })}
              <button type="submit" disabled={isSubmitting}>
                Ajoute Restoran
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default AddRestaurantForm;
