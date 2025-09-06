"use client";
import { useAuth } from "../context/AuthContext";
import withAuth from "../components/withAuth";

function Home() {
    const { logout } = useAuth();

    const handleLogout = () => {
        logout();
    };

    return (
        <div style={{ padding: "20px" }}>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "20px",
                }}
            >
                <h1>Welcome to Home Page</h1>
                <button
                    onClick={handleLogout}
                    style={{
                        padding: "10px 20px",
                        backgroundColor: "#dc3545",
                        color: "white",
                        border: "none",
                        borderRadius: "5px",
                        cursor: "pointer",
                    }}
                >
                    Logout
                </button>
            </div>
            <p>You are now authenticated and can access this protected page!</p>
        </div>
    );
}

export default withAuth(Home);
