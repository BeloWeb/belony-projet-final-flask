import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useSnackbar } from "notistack";
import { UserContext } from "../UserContext";
import { useGoogleLogin } from "@react-oauth/google";

const SignUp = () => {
  const navigate = useNavigate();
  const { updateUser } = useContext(UserContext);
  const [isSignUp, setIsSignUp] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  const loginSchema = Yup.object().shape({
    username: Yup.string().required("Required"),
    password: Yup.string().required("Required"),
  });

  const signUpSchema = Yup.object().shape({
    email: Yup.string().email("Invalid email").required("Required"),
    username: Yup.string().required("Required"),
    password: Yup.string().required("Required"),
  });

  const loginWithGoogle = useGoogleLogin({
    onSuccess: (codeResponse) => {
      fetch("/login/google", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ access_token: codeResponse.access_token }),
      })
        .then((resp) => resp.json())
        .then((data) => {
          if (data.id) {
            updateUser(data);
            navigate(`/profile/${data.id}`);
            enqueueSnackbar("Login successful!", { variant: "success" });
          } else {
            enqueueSnackbar("Failed to authenticate with Google.", {
              variant: "error",
            });
          }
        })
        .catch((err) => {
          enqueueSnackbar("An error occurred during Google login.", {
            variant: "error",
          });
        });
    },
    onError: (errorResponse) => {
      console.error("Google login error:", errorResponse);
      enqueueSnackbar("Google login failed.", { variant: "error" });
    },
  });

  const handleSubmit = async (values, { setSubmitting }) => {
    const endpoint = isSignUp ? "/food_users" : "/login";

    setSubmitting(true);
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((resp) => resp.json())
      .then((data) => {
        if (data.id) {
          updateUser(data); // Update the UserContext with new user information
          navigate(`/profile/${data.id}`);
          enqueueSnackbar(
            isSignUp ? "Sign up successful!" : "Login successful!",
            { variant: "success" }
          );
        } else {
          const message = data.message.startsWith("(sqlite3.IntegrityError)")
            ? "username already in use"
            : data.message;
          enqueueSnackbar(message, { variant: "error" }); // Handle errors
        }
      })
      .catch((err) => {
        enqueueSnackbar("An error occurred during login.", {
          variant: "error",
        });
      })
      .finally(() => setSubmitting(false));
  };

  return (
    <div className="signup-container">
      <div className="sign-image"></div>
      <div className="signup-box">
        <h2 className="form-title">{isSignUp ? "Sign Up" : "Login"}</h2>
        <Formik
          initialValues={{ email: "", username: "", password: "" }}
          validationSchema={isSignUp ? signUpSchema : loginSchema}
          onSubmit={handleSubmit}>
          {({ isSubmitting }) => (
            <Form className="signup-form">
              {isSignUp && (
                <>
                  <Field name="email" type="email" placeholder="Email" />
                  <ErrorMessage
                    name="email"
                    component="div"
                    className="form-error"
                  />
                </>
              )}
              <Field name="username" type="text" placeholder="Username" />
              <ErrorMessage
                name="username"
                component="div"
                className="form-error"
              />
              <Field name="password" type="password" placeholder="Password" />
              <ErrorMessage
                name="password"
                component="div"
                className="form-error"
              />
              <button
                type="submit"
                className="submit-btn"
                disabled={isSubmitting}>
                {isSignUp ? "Sign Up" : "Login"}
              </button>
            </Form>
          )}
        </Formik>
        <div className="login-options">
          {isSignUp ? (
            <p>
              Ou deja gen yon kont ?{" "}
              <span className="link" onClick={() => setIsSignUp(false)}>
                Konekte la
              </span>
            </p>
          ) : (
            <p>
              Ou nouvo sou Woody Vert - Restoran ?{" "}
              <span className="link" onClick={() => setIsSignUp(true)}>
                Kreye yon kont gratis la
              </span>
            </p>
          )}
          <div className="social-login">
            <p>Oubyen konekte la</p>
            <button className="google-btn" onClick={loginWithGoogle}>
              Google
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
