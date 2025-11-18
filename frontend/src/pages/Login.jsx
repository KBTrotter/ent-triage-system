import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const { login } = useAuth();
    const navigate = useNavigate(); 

    const handleAdminLogin = () => {
        login("adminUser", "admin");
        console.log("Admin user logged in");
        navigate("/dashboard");
    };
    
    const handleUserLogin = () => {
        login("regularUser", "user");
        console.log("Regular user logged in");
        navigate("/dashboard");
    };

    return (
        <div>
            <h1>Login Page</h1>
            <button onClick={handleAdminLogin}>Login as Admin</button>
            <button onClick={handleUserLogin}>Login as User</button>
        </div>
    );
}