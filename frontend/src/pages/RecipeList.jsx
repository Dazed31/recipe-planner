import { useState } from "react";
import { Link } from "react-router-dom";
import { useFetch } from "../hooks/useFetch";

function RecipeList() {
  const [page, setPage] = useState(1);
  const perPage = 6;

  const { data, loading, error } = useFetch(`/recipes?page=${page}&per_page=${perPage}`);

  if (loading) return <p className="status-text">Loading recipes...</p>;
  if (error) return <p className="status-text error-text">Error: {error}</p>;
  if (!data || data.items.length === 0) {
    return <p className="status-text">No recipes yet. Be the first to add one!</p>;
  }

  return (
    <div className="recipe-list-page">
      <h2>Recipes</h2>
      <div className="recipe-grid">
        {data.items.map((recipe) => (
          <Link to={`/recipes/${recipe.id}`} key={recipe.id} className="recipe-card">
            <h3>{recipe.title}</h3>
            <p className="recipe-meta">
              by {recipe.author?.username} · {recipe.prep_time} min
            </p>
            <p className="recipe-ingredient-count">
              {recipe.recipe_ingredients.length} ingredients
            </p>
          </Link>
        ))}
      </div>

      <div className="pagination">
        <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
          Previous
        </button>
        <span>
          Page {data.page} of {data.total_pages}
        </span>
        <button disabled={page >= data.total_pages} onClick={() => setPage((p) => p + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}

export default RecipeList;