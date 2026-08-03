import { useParams, useNavigate } from "react-router-dom";
import { useFetch } from "../hooks/useFetch";
import { useAuth } from "../hooks/useAuth";

const API_URL = import.meta.env.VITE_API_URL;

function RecipeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, token } = useAuth();

  const { data: recipe, loading, error } = useFetch(`/recipes/${id}`);

  const isOwner = recipe && user && String(recipe.user_id) === String(user.id);
  const canManage = isOwner || user?.role === "admin";

  const handleDelete = async () => {
    if (!window.confirm("Delete this recipe? This cannot be undone.")) return;

    const res = await fetch(`${API_URL}/recipes/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (res.ok || res.status === 204) {
      navigate("/recipes");
    } else {
      const body = await res.json().catch(() => null);
      alert(body?.error || "Failed to delete recipe");
    }
  };

  if (loading) return <p className="status-text">Loading recipe...</p>;
  if (error) return <p className="status-text error-text">Error: {error}</p>;
  if (!recipe) return null;

  return (
    <div className="recipe-detail-page">
      <h2>{recipe.title}</h2>
      <p className="recipe-meta">
        by {recipe.author?.username} · {recipe.prep_time} min
      </p>

      <h3>Ingredients</h3>
      <ul className="ingredient-list">
        {recipe.recipe_ingredients.map((ri) => (
          <li key={ri.id}>
            {ri.quantity} {ri.unit} {ri.ingredient.name}
          </li>
        ))}
      </ul>

      <h3>Instructions</h3>
      <p className="instructions">{recipe.instructions}</p>

      {canManage && (
        <div className="recipe-actions">
          <button onClick={() => navigate(`/recipes/${id}/edit`)}>Edit</button>
          <button onClick={handleDelete} className="danger">
            Delete
          </button>
        </div>
      )}
    </div>
  );
}

export default RecipeDetail;