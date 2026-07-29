import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { useFetch } from "../hooks/useFetch";

const API_URL = "http://localhost:5000";

function RecipeForm() {
  const { id } = useParams();
  const isEditing = Boolean(id);
  const navigate = useNavigate();
  const { token } = useAuth();

  const { data: existingRecipe } = useFetch(isEditing ? `/recipes/${id}` : null, {
    skip: !isEditing,
  });

  const { data: ingredientsData } = useFetch("/ingredients?page=1&per_page=50");

  const [title, setTitle] = useState("");
  const [instructions, setInstructions] = useState("");
  const [prepTime, setPrepTime] = useState("");
  const [ingredientRows, setIngredientRows] = useState([
    { ingredient_id: "", quantity: "", unit: "cup" },
  ]);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isEditing && existingRecipe) {
      setTitle(existingRecipe.title);
      setInstructions(existingRecipe.instructions);
      setPrepTime(existingRecipe.prep_time || "");
    }
  }, [isEditing, existingRecipe]);

  const updateRow = (index, field, value) => {
    setIngredientRows((rows) =>
      rows.map((row, i) => (i === index ? { ...row, [field]: value } : row))
    );
  };

  const addRow = () => {
    setIngredientRows((rows) => [...rows, { ingredient_id: "", quantity: "", unit: "cup" }]);
  };

  const removeRow = (index) => {
    setIngredientRows((rows) => rows.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      if (isEditing) {
        const res = await fetch(`${API_URL}/recipes/${id}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            title,
            instructions,
            prep_time: prepTime ? Number(prepTime) : null,
          }),
        });
        const body = await res.json();
        if (!res.ok) throw new Error(body.error || "Failed to update recipe");
        navigate(`/recipes/${id}`);
      } else {
        const ingredients = ingredientRows
          .filter((row) => row.ingredient_id && row.quantity)
          .map((row) => ({
            ingredient_id: Number(row.ingredient_id),
            quantity: Number(row.quantity),
            unit: row.unit,
          }));

        const res = await fetch(`${API_URL}/recipes`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            title,
            instructions,
            prep_time: prepTime ? Number(prepTime) : null,
            ingredients,
          }),
        });
        const body = await res.json();
        if (!res.ok) throw new Error(body.error || "Failed to create recipe");
        navigate(`/recipes/${body.id}`);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const availableIngredients = ingredientsData?.items || [];

  return (
    <div className="recipe-form-page">
      <h2>{isEditing ? "Edit Recipe" : "New Recipe"}</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Title
          <input value={title} onChange={(e) => setTitle(e.target.value)} required />
        </label>

        <label>
          Prep Time (minutes)
          <input
            type="number"
            value={prepTime}
            onChange={(e) => setPrepTime(e.target.value)}
            min="0"
          />
        </label>

        <label>
          Instructions
          <textarea
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
            rows={5}
            required
          />
        </label>

        {!isEditing && (
          <div className="ingredient-rows">
            <p className="field-label">Ingredients</p>
            {ingredientRows.map((row, i) => (
              <div className="ingredient-row" key={i}>
                <select
                  value={row.ingredient_id}
                  onChange={(e) => updateRow(i, "ingredient_id", e.target.value)}
                >
                  <option value="">Select ingredient</option>
                  {availableIngredients.map((ing) => (
                    <option key={ing.id} value={ing.id}>
                      {ing.name}
                    </option>
                  ))}
                </select>
                <input
                  type="number"
                  step="0.1"
                  placeholder="qty"
                  value={row.quantity}
                  onChange={(e) => updateRow(i, "quantity", e.target.value)}
                />
                <select value={row.unit} onChange={(e) => updateRow(i, "unit", e.target.value)}>
                  {["g", "kg", "ml", "l", "tsp", "tbsp", "cup", "fl_oz", "oz", "lb", "pinch"].map(
                    (u) => (
                      <option key={u} value={u}>
                        {u}
                      </option>
                    )
                  )}
                </select>
                <button
                  type="button"
                  className="remove-row"
                  onClick={() => removeRow(i)}
                  disabled={ingredientRows.length === 1}
                >
                  ✕
                </button>
              </div>
            ))}
            <button type="button" onClick={addRow} className="add-row">
              + Add ingredient
            </button>
          </div>
        )}

        {error && <p className="error-text">{error}</p>}

        <button type="submit" disabled={submitting}>
          {submitting ? "Saving..." : isEditing ? "Save Changes" : "Create Recipe"}
        </button>
      </form>
    </div>
  );
}

export default RecipeForm;