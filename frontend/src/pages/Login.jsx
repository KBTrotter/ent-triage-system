import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as Yup from "yup";
import React from "react";
import { deepPurple } from "@mui/material/colors";
import {
  Button,
  Box,
  Card,
  CardContent,
  TextField,
  Typography,
  FormControl,
  InputLabel,
  InputAdornment,
  OutlinedInput,
  IconButton,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";

export default function Login() {
  const formik = useFormik({
    initialValues: {
      username: "",
      password: "",
    },
    validationSchema: Yup.object({
      username: Yup.string().required("Username is required"),
      password: Yup.string().required("Password is required"),
    }),
    onSubmit: async (values) => {
      console.log(values);
      await new Promise((r) => setTimeout(r, 500));
      login(values.username, values.password);
      navigate("/dashboard");
      setSubmitting(false);
      resetForm();
    },
  });

  const [showPassword, setShowPassword] = React.useState(false);

  const handleClickShowPassword = () => {
    setShowPassword((prev) => !prev);
  };

  const handleForgotPassword = () => {
    console.log("Forgot Password clicked");
  };

  const { login } = useAuth();
  const navigate = useNavigate();

  // For testing purposes only
  // const handleAdminLogin = () => {
  //   login("adminUser", "password", "admin");
  //   console.log("Admin user logged in");
  //   navigate("/dashboard");
  // };

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: deepPurple[50],
      }}>
      <Card sx={{ width: 350, padding: 2 }}>
        <CardContent
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 2,
            textAlign: "center",
            padding: 2,
          }}>
          <Typography variant="h5" fontWeight="bold" sx={{ padding: 2 }}>
            Login
          </Typography>
          {/* Username */}
          <form onSubmit={formik.handleSubmit}>
            <TextField
              name="username"
              label="Username"
              variant="outlined"
              value={formik.values.username}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.username && Boolean(formik.errors.username)}
              helperText={formik.touched.username && formik.errors.username}
              fullWidth
            />
            {/* Password */}
            <FormControl variant="outlined" fullWidth sx={{ mt: 2 }}>
              <InputLabel
                error={
                  formik.touched.password && Boolean(formik.errors.password)
                }>
                Password
              </InputLabel>

              <OutlinedInput
                name="password"
                type={showPassword ? "text" : "password"}
                value={formik.values.password}
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                error={
                  formik.touched.password && Boolean(formik.errors.password)
                }
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton onClick={handleClickShowPassword} edge="end">
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                }
                label="Password"
              />

              {formik.touched.password && formik.errors.password && (
                <Typography
                  variant="caption"
                  color="error"
                  sx={{
                    marginTop: "3px",
                    marginLeft: "12px",
                    textAlign: "left",
                  }}>
                  {formik.errors.password}
                </Typography>
              )}
            </FormControl>

            <Button
              type="submit"
              sx={{
                backgroundColor: deepPurple[500],
                "&:hover": { backgroundColor: deepPurple[700] },
                color: "#fff",
                borderRadius: 3,
                mt: 2,
                width: "100%",
                textTransform: "none",
              }}>
              Log In
            </Button>
            <Button
              variant="text"
              disableRipple
              onClick={handleForgotPassword}
              sx={{
                textTransform: "none",
                "&:hover": {
                  backgroundColor: "transparent",
                  color: deepPurple[800],
                },
                color: deepPurple[400],
                mt: 2,
              }}>
              Forgot Password?
            </Button>
          </form>
          {/* This is for admin role testing purposes only */}
          {/* <button onClick={handleAdminLogin}>Login as Admin</button> */}
        </CardContent>
      </Card>
    </Box>
  );
}
