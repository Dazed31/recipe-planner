import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="navbar">
      <Link to="/recipes" className="navbar-brand">
        Recipe Planner
      </Link>
      <div className="navbar-links">
        {user && (
          <>
            <span className="navbar-user">
              {user.username} {user.role === "admin" && <span className="badge">admin</span>}
            </span>
            <Link to="/recipes/new">New Recipe</Link>
            <button onClick={handleLogout}>Log Out</button>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;