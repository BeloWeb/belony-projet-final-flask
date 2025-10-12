import React, { useContext, useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useSnackbar } from "notistack";
import { UserContext } from "../UserContext";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../RestaurantDetails.css";

const RestaurantDetails = () => {
  const { currentUser } = useContext(UserContext);
  const { id } = useParams();
  const [editingReview, setEditingReview] = useState(null);
  const [isEdit, setIsEdit] = useState(false);

  const [restaurant, setRestaurant] = useState({
    name: "",
    image_url: "",
    rating: "",
    phone_number: "",
    address: "",
    reviews: [],
    favorited_by: [],
    food_users: [],
  });
  const [showReviewForm, setShowReviewForm] = useState(false);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    fetchRestaurantDetails();
  }, [id]);

  const fetchRestaurantDetails = () => {
    fetch(`/restaurants/${id}`)
      .then((resp) => resp.json())
      .then((restaurantObj) => {
        setRestaurant(restaurantObj);
        const userReview = restaurantObj.reviews.find(
          (review) => review.food_user_id === currentUser?.id
        );
        setEditingReview(userReview || null);
      })
      .catch((error) => {
        enqueueSnackbar(`Error: ${error.message}`, { variant: "error" });
      });
  };

  const handleSaveFavorite = () => {
    if (!currentUser) {
      enqueueSnackbar("You must be logged in to add a favorite.", {
        variant: "warning",
      });
      return;
    }

    fetch(`/favorites`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ restaurant_id: id }),
    })
      .then((response) => response.json())
      .then(() => {
        fetchRestaurantDetails();
        enqueueSnackbar("Favorite added successfully!", { variant: "success" });
      })
      .catch((error) => {
        enqueueSnackbar(error.message, { variant: "error" });
      });
  };

  const handleDeleteFavorite = () => {
    fetch(`/favorites/${id}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then(() => {
        fetchRestaurantDetails();
        enqueueSnackbar("Favorite removed successfully!", {
          variant: "success",
        });
      })
      .catch((error) => {
        enqueueSnackbar(error.message, { variant: "error" });
      });
  };

  const handleEditReview = (review) => {
    setIsEdit(true); // Indicates we're in edit mode
    setEditingReview(review); // Set the current review we're editing
    setShowReviewForm(true); // Show the review form
  };

  const handleCancelEdit = () => {
    setIsEdit(false);
    setEditingReview(null);
    setShowReviewForm(false);
  };

  const handleDeleteReview = (reviewId) => {
    fetch(`/reviews/${reviewId}`, { method: "DELETE" })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to delete review");
        setEditingReview(null);
        setShowReviewForm(false);
        fetchRestaurantDetails();
        enqueueSnackbar("Review deleted successfully!", {
          variant: "success",
        });
      })
      .catch((error) => {
        enqueueSnackbar(error.message, { variant: "error" });
      });
  };

  const reviewSchema = Yup.object().shape({
    content: Yup.string().required("Content is required"),
    rating: Yup.number().min(1).max(5).required("Rating is required"),
  });

  const handleAddOrEditReview = (values, { setSubmitting }) => {
    if (!currentUser) {
      enqueueSnackbar("You must be logged in to add or edit a review.", {
        variant: "error",
      });
      return;
    }

    if (
      !editingReview &&
      restaurant.reviews.some(
        (review) => review.food_user_id === currentUser.id
      )
    ) {
      enqueueSnackbar(
        "You have already submitted a review for this restaurant.",
        { variant: "error" }
      );
      return;
    }

    const reviewData = {
      ...values,
      restaurant_id: id,
      food_user_id: currentUser.id,
    };

    const method = editingReview ? "PATCH" : "POST";
    const endpoint = editingReview
      ? `/reviews/${editingReview.id}`
      : "/reviews";

    fetch(endpoint, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reviewData),
    })
      .then((response) => response.json())
      .then(() => {
        fetchRestaurantDetails();
        enqueueSnackbar(
          editingReview
            ? "Review updated successfully!"
            : "Review added successfully!",
          { variant: "success" }
        );
        // Reset the editing states after successful submission
        setEditingReview(null);
        setIsEdit(false); // Add this line
        setShowReviewForm(false); // If you want to close the form as well
      })
      .catch((error) => {
        enqueueSnackbar(error.message, { variant: "error" });
      })
      .finally(() => setSubmitting(false));
  };

  const reviewList = restaurant.reviews.map((review, index) => (
    <li key={index}>
      {review.content} - {review.rating} stars
      {currentUser && currentUser.id === review.food_user_id && (
        <>
          {isEdit && editingReview && editingReview.id === review.id ? (
            <>
              <button onClick={() => handleDeleteReview(review.id)}>
                Efase
              </button>
              <button onClick={handleCancelEdit}>Anile</button>
            </>
          ) : (
            <>
              <button onClick={() => handleEditReview(review)}>Modifye</button>
            </>
          )}
        </>
      )}
    </li>
  ));
  const toggleReviewForm = () => {
    if (
      editingReview ||
      !restaurant.reviews.some(
        (review) => review.food_user_id === currentUser?.id
      )
    ) {
      setShowReviewForm(!showReviewForm);
    }
  };

  const isFavorite = restaurant.favorited_by.includes(currentUser?.username);

  return (
    <div className="one_restaurant">
      <div className="image-container">
        <img src={restaurant.image_url} alt={restaurant.name} />
        <div className="image-details">
          <h2>{restaurant.name}</h2>
          <Link to={`/view-menu/${id}`}>Gade Meni</Link>
          <p>Nòt: {restaurant.rating}</p>
          <p>Nimewo Telefòn: {restaurant.phone_number}</p>
        </div>
      </div>

      <div className="reviews-container">
        {currentUser && (
          <>
            {isFavorite ? (
              <button onClick={handleDeleteFavorite}>Retire favori</button>
            ) : (
              <button onClick={handleSaveFavorite}>Ajoute favori</button>
            )}
            {!showReviewForm &&
              !restaurant.reviews.some(
                (review) => review.food_user_id === currentUser.id
              ) && (
                <button onClick={() => setShowReviewForm(true)}>
                  Nòt Restoran
                </button>
              )}
          </>
        )}
        {showReviewForm && (
          <Formik
            initialValues={{
              content: editingReview?.content || "",
              rating: editingReview?.rating || "",
            }}
            validationSchema={reviewSchema}
            onSubmit={handleAddOrEditReview}
            enableReinitialize>
            {({ isSubmitting }) => (
              <Form>
                <Field
                  name="content"
                  as="textarea"
                  placeholder="Write your review here"
                />
                <ErrorMessage name="content" component="div" />
                <Field
                  name="rating"
                  type="number"
                  placeholder="Rating (1-5)"
                  min="1"
                  max="5"
                />
                <ErrorMessage name="rating" component="div" />
                <button type="submit" disabled={isSubmitting}>
                  {editingReview ? "Update Review" : "Submit Review"}
                </button>
              </Form>
            )}
          </Formik>
        )}
        <ul>{reviewList}</ul>
      </div>

      <aside className="favorites-container">
        <h3>Itilizatè ki favorize Restoran:</h3>
        <ul>
          {/* List of users who favorited */}
          {restaurant.favorited_by.map((username, index) => (
            <li key={index}>{username}</li>
          ))}
        </ul>
      </aside>
    </div>
  );
};

export default RestaurantDetails;
