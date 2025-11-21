import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import React from "react";
import { deepPurple } from "@mui/material/colors";
import { Button, Box, Card, CardContent, TextField, Typography, FormControl, InputLabel, InputAdornment, OutlinedInput, IconButton} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
export default function Login() {
    const { login } = useAuth();
    const navigate = useNavigate(); 

    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");

    const [usernameError, setUsernameError] = React.useState(false);
    const [passwordError, setPasswordError] = React.useState(false);

    const [showPassword, setShowPassword] = React.useState(false);
    const handleClickShowPassword = () => setShowPassword((show) => !show);

    // For testing purposes only
    // const handleAdminLogin = () => {
    //     login("adminUser", "admin");
    //     console.log("Admin user logged in");
    //     navigate("/dashboard");
    // };
    

    const handleLogin = (u) => {
        let hasError = false;
        //check for empty fields -> error if empty
        if (username.trim() === "") {
            setUsernameError(true);
            hasError = true;
        } else {
            setUsernameError(false);
        }
        if(password.trim() === "") {
            setPasswordError(true);
            hasError = true;
        } else {
            setPasswordError(false);
        }
        if (hasError) {
            return;
        }
        //user login
        login(username, password);
        navigate("/dashboard");
        console.log("Login button clicked");
    };


    return (
        <Box sx={{
                height: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                backgroundColor: deepPurple[50],
            }}>
            <Card sx={{ width: 350, padding: 2 }}>
                <CardContent sx={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 2,
                        textAlign: "center",
                        padding: 2
                    }}>
                    <Typography variant="h5" fontWeight="bold" sx={{padding: 2}}>Login</Typography>
                    {/* Username */}
                    <TextField 
                      label="Username" 
                      variant="outlined" 
                      value={username} 
                      onChange={(e) => setUsername(e.target.value)} 
                      error={usernameError} 
                      helperText={usernameError ? "Username is required": ""}
                    />

                    {/* Password */}
                    <FormControl  variant="outlined">
                      <InputLabel error={passwordError}>Password</InputLabel>
                      <OutlinedInput
                        type={showPassword ? 'text' : 'password'}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        error={passwordError} 
                        endAdornment={
                          <InputAdornment position="end">
                            <IconButton
                              onClick={handleClickShowPassword}
                              edge="end"
                            >
                              {showPassword ? <VisibilityOff /> : <Visibility />}
                            </IconButton>
                          </InputAdornment>
                        }
                        label="Password"
                      />
                      {passwordError && (
                        <Typography variant="caption" color="error"  sx={{ marginTop: "4px", textAlign: "left" , marginLeft: "14px"}}>
                          Password is required
                        </Typography>
                      )}
                    </FormControl> 
                    {/* Login Buttons*/}
                    <Button onClick={handleLogin} 
                      sx={{
                        backgroundColor: deepPurple[500],
                        "&:hover": { backgroundColor: deepPurple[700] },
                        color: "#fff",
                        borderRadius: 3,
                      }}>
                        Log In
                      </Button>
                    <Button
                      variant="text" 
                      disableRipple 
                      sx={{ 
                        textTransform: "none", 
                        "&:hover": { backgroundColor: "transparent", color: deepPurple[800] }, 
                        color: deepPurple[400] 
                      }}
                      onClick={() => console.log("Forgot Password clicked")}>Forgot Password?</Button>
                    {/* This is for admin role testing purposes only
                    <button onClick={handleAdminLogin}>Login as Admin</button>*/}
                </CardContent>
            </Card>
        </Box>
    );
}